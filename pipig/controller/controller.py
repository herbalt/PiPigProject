from generics.constants import COMPONENT_TYPE_SENSOR, COMPONENT_TYPE_DATAPOINT, COMPONENT_TYPE_DATAPOINTS_APPLIANCE_BINDER
from pipig.generics.models import GenericReading
from pipig.curing_sessions.models import CuringSession
from pipig.recipes.models import Recipe
from pipig.general.patterns import Subject, Observer
from pipig.factories.abstract_factory import AbstractFactory
from pipig.processors.factory import ProcessorChainFactory, PRINT_DATABASE
from Queue import Queue
from threading import Thread, Event
from pipig import app
from pipig.utilities import debug_messenger


class Controller(Observer, Subject):
    """
    Container for creating and binding all the Objects in a Recipe
    Input Queue takes Processed Sensor readings
    Processes the Queue by comparing against datapoints to build a New Reading for the Appliance
    Pass the Appliance Reading to another Queue that is pushes results to the relevant appliances
    """

    def __init__(self, recipe_id, curing_session_id=None):
        super(Controller, self).__init__()

        self.recipe_id = recipe_id
        self.curing_session_id = curing_session_id
        self.factory = AbstractFactory()

        self.sensors_dict = {}
        self.appliances_dict = {}
        self.datapoints_dict = {}
        self.appliance_binders_dict = {}

        processor_factory = ProcessorChainFactory()
        self.sensor_processor = processor_factory.build_object(PRINT_DATABASE)
        self.appliance_processor = processor_factory.build_object(PRINT_DATABASE)

        self.sensor_queue = Queue()
        self.sensor_queue.empty()
        self.appliance_queue = Queue()
        self.sensor_queue.empty()


        self.build_controller()

    """
    GET Methods
    """

    def get_recipe_id(self):
        return self.recipe_id

    def get_curing_session_id(self):
        return self.curing_session_id

    def get_recipe_obj(self):
        # with app.app_context():
        recipe = Recipe.get(self.get_recipe_id())
        return recipe

    def get_session_obj(self):
        if self.get_curing_session_id() is None:
            return CuringSession("GenericSession")
        else:
            # with app.app_context():
            session = CuringSession.get(self.get_curing_session_id())
            if session is None:
                return CuringSession("GenericSession")
            return CuringSession.get(self.get_curing_session_id())

    """
    Build Methods
    """

    def build_controller(self):
        """
        Main method to call from init to construct the environment
        :return: 
        """
        self.build_objects()
        self.bind_sensor_objects()
        self.bind_appliance_objects()

    def build_objects(self):
        """
        Build all Sensors, Datapoints and Appliances
        :return: 
        """
        self.build_sensors()
        self.build_appliances()
        self.build_datapoints()
        self.build_appliance_binders()

    def build_sensors(self):
        """
        Build Sensors in a Dict
        :return: 
        """
        recipe_obj = self.get_recipe_obj()
        sensor_list = recipe_obj.get_sensor_ids()
        self.sensors_dict = self.factory.build_objects_dict(self.factory.SENSOR, sensor_list)
        for sensor_id in self.sensors_dict:
            sensor_object = self.sensors_dict.get(sensor_id)
            sensor_object.attach(self.sensor_processor)
            #self.sensor_processor.attach(sensor_object)
        debug_messenger("SENSORS: \n" + str(self.sensors_dict))
        return self.sensors_dict

    def build_appliances(self):
        """
        Build Appliances in a Dict
        :return: 
        """
        self.appliances_dict = self.factory.build_objects_dict(self.factory.APPLIANCE, self.get_recipe_obj().get_appliance_ids())
        for appliance_id in self.appliances_dict:
            appliance_object = self.appliances_dict.get(appliance_id)
            appliance_object.attach(self.appliance_processor)
            # self.appliance_processor.attach(appliance_object)
        debug_messenger("APPLIANCES: \n" + str(self.appliances_dict))
        return self.appliances_dict

    def build_datapoints(self):
        """
        Build Datapoints in a Dict
        :return: 
        """
        return self.factory.build_objects_dict(self.factory.DATAPOINTS, self.get_recipe_obj().get_datapoints_ids())

    def build_appliance_binders(self):
        return self.factory.build_objects_dict(self.factory.APPLIANCE_BINDER, self.get_recipe_obj().get_appliance_datapoints_binding_ids())

    def bind_sensor_objects(self):
        """
        Bind Sensor Objects to Controller
        :return: 
        """
        self.sensor_processor.attach(self)



    def bind_appliance_objects(self):
        """
        NOT SURE IF I NEED THIS FUNCTION .... HOWEVER I DO MAKE AN EXPLICIT CALL TO THE RELEVANT APPLIANCE
        Bind Processors to Appliances
        then
        Bind Controller to Appliances
        :return: 
        """

        # self.attach(self.appliance_processor)
        pass

    """
    Abstract Methods
    """
    def receive(self, result, status_code=0):
        """
        Receive a Sensor Reading to the Controller
        :param result: A Sensor Reading
        :param status_code: 
        :return: 
        """
        self.add_sensor_reading_to_queue(result, status_code)

    """
    Queue Management
    """

    def start_sensor_queue_processing(self):
        """
        Begins the Thread for processing the incoming Sensor Readings
        :return: 
        """
        num_threads = 3

        for i in range(num_threads):
            # worker = Thread(target=self.process_sensor_queue, args=(self.sensor_queue,))
            worker = Thread(target=self.process_sensor_queue)
            worker.setDaemon(True)
            worker.start()

    def start_appliance_queue_processing(self):
        """
        Begins the Thread for processing the outgoing Appliance Readings
        :return: 
        """
        num_threads = 3

        for i in range(num_threads):
            # worker = Thread(target=self.process_appliance_queue, args=(self.appliance_queue,))
            worker = Thread(target=self.process_appliance_queue)
            worker.setDaemon(True)
            worker.start()

    def stop_sensor_queue_processing(self):
        """
        Stops the Sensor Queue from receiving Sensor Readings
        :return: 
        """
        # self.add_sensor_reading_to_queue(Event())
        self.sensor_queue.join()

    def stop_appliance_queue_processing(self):
        """
        Stops the Appliance Queue from receiving Appliance Readings
        :return: 
        """
        self.appliance_queue.join()

    """
    Interactions
    """

    def start_sensors(self):
        """
        Start every sensor in the list of Sensors
        :return: 
        """
        debug_messenger("START SENSORS")
        for sensor_id in self.sensors_dict:
            sensor_obj = self.sensors_dict.get(sensor_id)
            sensor_obj.execute_operation()

        pass

    def stop_sensors(self):
        """
        Stop every sensor in the list of Sensors
        :return: 
        """
        for sensor_id in self.sensors_dict:
            sensor_obj = self.sensors_dict.get(sensor_id)
            sensor_obj.cancel_operation()


    def add_sensor_reading_to_queue(self, reading, status_code=0):
        """
        Takes the reading and add it to the Sensor Reading Queue
        :param reading: A processed Sensor reading that is Recieved
        :return: 
        """
        debug_messenger("ADD SENSOR READING TO QUEUE")
        self.sensor_queue.put_nowait(reading)

    def process_sensor_queue(self):

        appliance_reading_list = []

        sensor_reading = self.sensor_queue.get()
        debug_messenger("PROCESS SENSOR QUEUE" + str(sensor_reading))
        with app.app_context():
            datapoints_result_list = self.process_sensor_reading(sensor_reading)
        for datapoint in datapoints_result_list:
            datapoint_list = self.process_datapoint_results_to_appliance(datapoint)
            for datapoint in datapoint_list:
                appliance_reading_list.append(datapoint)
        for appliance_reading in appliance_reading_list:
            self.add_appliance_reading_to_queue(appliance_reading)

    def process_sensor_reading(self, sensor_reading):
        """
        Take a Sensor Reading from the Queue and build an output Reading based on the interaction with the Datapoints
        :return: The Output Reading(s) that will be sent to the Appliance Queue
        """
        debug_messenger("PROCESS SENSOR READING")
        # Check if Reading is of the right component type
        if not sensor_reading.get_component_type_id() == COMPONENT_TYPE_SENSOR:
            raise AttributeError

        # Get the relevant readings to be able to compare against a datapoints object
        recipe = self.get_recipe_obj()
        session = self.get_session_obj()
        sensor_id = sensor_reading.get_component_id()
        reading_timestamp = sensor_reading.get_timestamp()
        start_time = session.get_start_time()
        time_elapsed = reading_timestamp - start_time
        reading_value = sensor_reading.get_value()

        # Get all the corresponding datapoints to compare with
        datapoint_id_list = recipe.get_datapoints_for_sensor(sensor_id)

        datapoint_result_list = []

        for datapoint_id in datapoint_id_list:
            datapoints = self.datapoints_dict.get(datapoint_id)

            # Compare Sensor reading versus all the corresponding datapoints
            datapoint = datapoints.get_point(time_elapsed)

            compare_result = reading_value - datapoint.get_value()
            datapoint_result_list.append(GenericReading(datapoint_id, COMPONENT_TYPE_DATAPOINT, compare_result, reading_timestamp))

            # Create a Reading for every datapoint comparision that will be added to the Appliance Queue

        # Return the list of Output Readings

        for datapoint_result in datapoint_result_list:
            recipe.get_appliances_for_datapoint(datapoint_result.get_component_id())

        return datapoint_result_list

    def process_datapoint_results_to_appliance(self, datapoint_readings):
        debug_messenger("PROCESS DATAPOINT RESULTS TO APPLIANCE")
        if not datapoint_readings.get_component_id() == COMPONENT_TYPE_DATAPOINT:
            raise AttributeError

        recipe = self.get_recipe_obj()
        binder_list = recipe.get_appliance_datapoints_binding_ids()

        for binder in binder_list:
            if binder.get_datapoint_id() == datapoint_readings.get_component_id():
                binder_obj = self.appliance_binders_dict.get(binder.get_id())
                polarity = binder_obj.get_polarity()
                appliance_response = self.response_to_datapoint(datapoint_readings.get_value(), polarity)
                output_reading = GenericReading(binder_obj.get_appliance_id(), COMPONENT_TYPE_DATAPOINTS_APPLIANCE_BINDER, appliance_response,
                               datapoint_readings.get_timestamp())
                self.add_appliance_reading_to_queue(output_reading)

    def response_to_datapoint(self, diff_sensor_datapoint_value, polarity):
        if diff_sensor_datapoint_value < 0:
            return polarity
        elif diff_sensor_datapoint_value > 0:
            return -1 * polarity
        else:
            return 0

    def add_appliance_reading_to_queue(self, reading):
        """
        Add the Appliance Reading to the Appliance Queue
        :param reading: A output reading that is to be processed by the Appliances
        :return: 
        """
        debug_messenger("ADD APPLIANCE READING TO QUEUE")
        if not reading.get_component_id() == COMPONENT_TYPE_DATAPOINTS_APPLIANCE_BINDER:
            raise AttributeError

        self.appliance_queue.put_nowait(reading)


    def process_appliance_queue(self):
        """
        Take a Appliance Reading from the Queue and send to the relevant Appliance Objects
        :return: 
        """
        debug_messenger("PROCESS APPLIANCE QUEUE")
        appliance_reading = self.appliance_queue.get()
        for appliance_id in self.appliances_dict:
            appliance_obj = self.appliances_dict[appliance_id]
            if appliance_obj.get_id() == appliance_reading:
                appliance_obj.recieve(appliance_reading)




