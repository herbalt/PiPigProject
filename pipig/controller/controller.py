from generics.constants import COMPONENT_TYPE_SENSOR, COMPONENT_TYPE_DATAPOINT, \
    COMPONENT_TYPE_DATAPOINTS_APPLIANCE_BINDER
from pipig.generics.models import GenericReading
from pipig.curing_sessions.models import CuringSession
from pipig.recipes.models import Recipe
from pipig.general.patterns import Subject, Observer
from pipig.factories.abstract_factory import AbstractFactory
from pipig.processors.factory import ProcessorChainFactory, DATABASE_ONLY, PRINT_PROCESSOR
from queues.queues import BaseQueue
from threading import Thread, ThreadError
from pipig import app
from pipig.utilities import debug_messenger


class Controller(Observer, Subject):
    """
    Container for creating and binding all the Objects in a Recipe
    Input Queue takes Processed Sensor readings
    Processes the Queue by comparing against datapoints to build a New Reading for the Appliance
    Pass the Appliance Reading to another Queue that is pushes results to the relevant appliances
    """

    def __init__(self, recipe_id, curing_session_id=None, processor_type=DATABASE_ONLY):
        super(Controller, self).__init__()

        # Store init parameters
        self.recipe_id = recipe_id
        self.curing_session_id = curing_session_id

        # Prepare the Queues for Reading entries
        self.sensor_queue = BaseQueue()
        self.appliance_queue = BaseQueue()

        # Prepare Base Objects
        self.factory = AbstractFactory()

        # Prepare Empty Object Lists
        self.sensors_dict = {}
        self.appliances_dict = {}
        self.datapoints_dict = {}
        self.appliance_binders_dict = {}

        # Prepare Processors
        processor_factory = ProcessorChainFactory()
        self.sensor_processor = processor_factory.build_object(processor_type)
        self.appliance_processor = processor_factory.build_object(processor_type)

        # Configure Object
        self.build_controller()

    """
    GET Methods
    """
    def get_recipe_id(self):
        return self.recipe_id

    def get_curing_session_id(self):
        return self.curing_session_id

    def get_recipe_obj(self):
        recipe = Recipe.get(self.get_recipe_id())
        return recipe

    def get_session_obj(self):
        if self.get_curing_session_id() is None:
            return CuringSession("GenericSession")
        else:
            session = CuringSession.get(self.get_curing_session_id())
            if session is None:
                return CuringSession("GenericSession")
            return CuringSession.get(self.get_curing_session_id())

    def get_sensor_objects(self):
        sensor_list = []
        for sensor_id in self.sensors_dict.keys():
            sensor_list.append(self.sensors_dict.get(sensor_id))
        return sensor_list

    def get_appliance_objects(self):
        appliance_list = []
        for appliance_id in self.appliances_dict.keys():
            appliance_list.append(self.appliances_dict.get(appliance_id))
        return appliance_list


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
        debug_messenger("SENSORS: \n" + str(self.sensors_dict))
        return self.sensors_dict

    def configure_sensor_gpios(self):
        pass

    def build_appliances(self):
        """
        Build Appliances in a Dict
        :return: 
        """
        appliance_list = self.get_recipe_obj().get_appliance_ids()
        self.appliances_dict = self.factory.build_objects_dict(self.factory.APPLIANCE, appliance_list)
        for appliance_id in self.appliances_dict:
            appliance_object = self.appliances_dict.get(appliance_id)
            appliance_object.attach(self.appliance_processor)
        debug_messenger("APPLIANCES: \n" + str(self.appliances_dict))
        return self.appliances_dict

    def build_datapoints(self):
        """
        Build Datapoints in a Dict
        :return: 
        """
        recipe_obj = self.get_recipe_obj()
        datapoints_list = recipe_obj.get_datapoints_ids()
        self.datapoints_dict = self.factory.build_objects_dict(self.factory.DATAPOINTS, datapoints_list)
        debug_messenger("DATAPOINTS: \n" + str(self.datapoints_dict))
        return self.datapoints_dict

    def build_appliance_binders(self):
        """
        Build Appliance Datapoint Binder in a Dict
        :return:
        """
        recipe_obj = self.get_recipe_obj()
        binders_list = recipe_obj.get_appliance_datapoints_binding_ids()
        self.appliance_binders_dict = self.factory.build_objects_dict(self.factory.APPLIANCE_BINDER,
                                                                      binders_list)
        debug_messenger("BINDERS: \n" + str(self.appliance_binders_dict))
        return

    def bind_sensor_objects(self):
        """
        Bind Sensor Objects to Controller
        :return: 
        """
        self.sensor_processor.attach(self)

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
    def thread_sensor_queue_processing(self):
        """
        Begins the Thread for processing the incoming Sensor Readings
        :return: 
        """
        debug_messenger("SENSOR QUEUE WORKER STARTED")

        num_threads = 2
        for i in range(num_threads):
            worker = Thread(target=self.process_sensor_queue)
            worker.setDaemon(True)
            try:
                worker.start()
            except ThreadError:
                debug_messenger("FAILED TO START SENSOR QUEUE: " + str(self.sensor_queue))

    def thread_appliance_queue_processing(self):
        """
        Begins the Thread for processing the outgoing Appliance Readings
        :return: 
        """
        debug_messenger("APPLIANCE QUEUE WORKER STARTED")

        num_threads = 2
        for i in range(num_threads):
            worker = Thread(target=self.process_appliance_queue)
            worker.setDaemon(True)
            try:
                worker.start()
            except ThreadError:
                debug_messenger("FAILED TO START APPLIANCE QUEUE: " + str(self.sensor_queue))

    def start_sensor_queue_processing(self):
        """
        Start the Sensor Queue from being able to take readings from the Queue
        :return:
        """
        self.sensor_queue.set_state(True)
        self.thread_sensor_queue_processing()

    def start_appliance_queue_processing(self):
        """
        Start the Appliance Queue from being able to take readings from the Queue
        :return:
        """
        self.appliance_queue.set_state(True)
        self.thread_appliance_queue_processing()

    def stop_sensor_queue_processing(self):
        """
        Stops the Sensor Queue from receiving Sensor Readings
        :return: 
        """
        self.sensor_queue.set_state(False)
        self.sensor_queue.join()

    def stop_appliance_queue_processing(self):
        """
        Stops the Appliance Queue from receiving Appliance Readings
        :return: 
        """
        self.appliance_queue.set_state(False)
        self.appliance_queue.join()

    """
    Interactions
    """

    def start(self):
        """
        Starts Sensors and Queues of the Controller
        :return:
        """

        self.start_sensors()
        self.start_sensor_queue_processing()
        self.start_appliance_queue_processing()

    def stop(self):
        """
        Stops the Sensors and Queues of the Controller
        :return:
        """
        self.stop_sensors()
        self.stop_sensor_queue_processing()
        self.stop_appliance_queue_processing()

    def start_sensors(self):
        """
        Start every serial_sensor in the list of Sensors
        :return: 
        """
        debug_messenger("START SENSORS\n\n")
        for sensor_id in self.sensors_dict:
            sensor_obj = self.sensors_dict.get(sensor_id)
            sensor_obj.execute_operation()

    def stop_sensors(self):
        """
        Stop every serial_sensor in the list of Sensors
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
        self.sensor_queue.put_nowait(reading)
        debug_messenger("1 - ADD SENSOR READING TO QUEUE: " + str(self.sensor_queue))

    def process_sensor_queue(self):
        """
        Continually take a Reading from the Queue and interact with the specific datapoints.
        Then create all the relevant Appliance readings to the Appliance Queue
        :return:
        """
        while self.sensor_queue.get_state():
            if self.sensor_queue.empty() is False:
                appliance_reading_list = []

                sensor_reading = self.sensor_queue.get()
                debug_messenger("2 -    PROCESS SENSOR QUEUE: " + str(sensor_reading))
                with app.app_context():

                    datapoints_result_list = self.process_sensor_reading(sensor_reading)

                    datapoint_list = []

                    # TODO ISSUES WITH THIS SECTION OF CODE DUE TO ITERATORS NOT CODED WELL
                    for datapoint in datapoints_result_list:
                        # datapoint_list.append(self.process_datapoint_results_to_appliance(datapoint))
                        datapoint_list = self.process_datapoint_results_to_appliance(datapoint)

                        if datapoint_list is not None:
                            for datapoint in datapoint_list:
                                appliance_reading_list.append(datapoint)

                    for appliance_reading in appliance_reading_list:
                        self.add_appliance_reading_to_queue(appliance_reading)

    def process_sensor_reading(self, sensor_reading):
        """
        Take a Sensor Reading from the Queue and build an output Reading based on the interaction with the Datapoints
        :return: The Output Reading(s) that will be sent to the Appliance Queue
        """

        # Check if Reading is of the right component type
        if not sensor_reading.get_component_type_id() == COMPONENT_TYPE_SENSOR:
            raise AttributeError

        with app.app_context():
            # Get the relevant readings to be able to compare against a datapoints object
            recipe = self.get_recipe_obj()
            session = self.get_session_obj()
            sensor_id = sensor_reading.get_component_id()
            reading_timestamp = sensor_reading.get_timestamp()
            start_time = session.get_start_time()
            time_elapsed = reading_timestamp - start_time
            reading_value = sensor_reading.get_value()

            # Store the Original Sensor Reading in the Database
            GenericReading.create(component_id=sensor_id,
                                  component_type_id=COMPONENT_TYPE_SENSOR,
                                  reading_value=reading_value,
                                  reading_timestamp=reading_timestamp,
                                  recipe_id=recipe.get_id())

            # Get all the corresponding datapoints to compare with
            datapoint_id_list = recipe.get_datapoints_for_sensor(sensor_id)

            datapoint_result_list = []
            datapoint_message_list = []

            for datapoint_id in datapoint_id_list:
                datapoints = self.datapoints_dict.get(datapoint_id)

                # Compare Sensor reading versus all the corresponding datapoints
                datapoint = datapoints.get_point(time_elapsed)

                compare_result = reading_value - datapoint.get_value()

                reading = GenericReading(datapoint_id, COMPONENT_TYPE_DATAPOINT, compare_result, reading_timestamp, self.get_recipe_id())
                datapoint_result_list.append(reading)
                datapoint_message_list.append(str(reading))

        debug_messenger("3 -        PROCESS SENSOR READING: " + str(datapoint_message_list))
        return datapoint_result_list

    def process_datapoint_results_to_appliance(self, datapoint_readings):
        """
        Take a Datapoint Reading and converts it to an Appliance reading and adds it to the Appliance Queue
        :param datapoint_readings:
        :return:
        """
        debug_messenger("4 -            PROCESS DATAPOINT RESULTS TO APPLIANCE: " + str(datapoint_readings))
        with app.app_context():
            if not datapoint_readings.get_component_type_id() == COMPONENT_TYPE_DATAPOINT:
                raise AttributeError

            recipe = self.get_recipe_obj()
            binder_list = recipe.get_appliance_datapoints_binding_ids()

            for binder in binder_list:
                binder_obj = self.appliance_binders_dict.get(binder)

                if binder_obj.get_datapoints_id() == datapoint_readings.get_component_id():
                    polarity = binder_obj.get_polarity()
                    appliance_response = self.response_to_datapoint(datapoint_readings.get_value(), polarity)
                    output_reading = GenericReading.create(component_id=binder_obj.get_appliance_id(),
                                                    component_type_id=COMPONENT_TYPE_DATAPOINTS_APPLIANCE_BINDER,
                                                    reading_value=appliance_response,
                                                    reading_timestamp=datapoint_readings.get_timestamp(),
                                                    recipe_id=self.get_recipe_id())
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
        # debug_messenger("ADD APPLIANCE READING TO QUEUE")
        if not reading.get_component_type_id() == COMPONENT_TYPE_DATAPOINTS_APPLIANCE_BINDER:
            raise AttributeError

        self.appliance_queue.put_nowait(reading)
        debug_messenger("5 -                ADD APPLIANCE READING TO QUEUE: " + str(self.appliance_queue))

    def process_appliance_queue(self):
        """
        Continually take a Appliance Reading from the Queue and send to the relevant Appliance Objects
        :return: 
        """
        while self.appliance_queue.get_state():
            appliance_reading = self.appliance_queue.get()
            debug_messenger("6 -                    PROCESS APPLIANCE QUEUE: " + str(appliance_reading))
            for appliance_id in self.appliances_dict:
                appliance_obj = self.appliances_dict[appliance_id]
                if appliance_obj.get_id() == appliance_reading.get_component_id():
                    appliance_obj.receive(appliance_reading)
