from generics.constants import COMPONENT_TYPE_SENSOR, COMPONENT_TYPE_DATAPOINT, COMPONENT_TYPE_DATAPOINTS_APPLIANCE_BINDER
from generics.models import GenericReading
from pipig.sessions.models import Session
from pipig.recipes.models import Recipe
from pipig.general.patterns import Subject, Observer
from pipig.factories.abstract_factory import AbstractFactory
from pipig.processors.factory import ProcessorChainFactory, PRINT_DATABASE
from Queue import Queue
from pipig.binders.models import BindDatapoitnsAppliances

class Controller(Observer, Subject):
    """
    Container for creating and binding all the Objects in a Recipe
    Input Queue takes Processed Sensor readings
    Processes the Queue by comparing against datapoints to build a New Reading for the Appliance
    Pass the Appliance Reading to another Queue that is pushes results to the relevant appliances
    """

    def __init__(self, recipe_id, session_id=None):
        super(Controller, self).__init__()

        self.recipe_id = recipe_id
        self.session_id = session_id
        self.factory = AbstractFactory()

        self.sensors_dict = {}
        self.appliances_dict = {}
        self.datapoints_dict = {}

        processor_factory = ProcessorChainFactory()
        self.sensor_processor = processor_factory.build_object(PRINT_DATABASE)
        self.appliance_processor = processor_factory.build_object(PRINT_DATABASE)

        self.sensor_queue = Queue()
        self.appliance_queue = Queue()

        self.build_controller()

    """
    GET Methods
    """

    def get_recipe_id(self):
        return self.recipe_id

    def get_session_id(self):
        return self.session_id

    def get_recipe_obj(self):
        recipe = Recipe.get(self.get_recipe_id())
        return recipe

    def get_session_obj(self):
        if self.get_session_id() is None:
            return Session("GenericSession")
        else:
            session = Session.get(self.get_session_id())
            if session is None:
                return Session("GenericSession")
            return Session.get(self.get_session_id())

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
        self.build_appliances()
        self.build_datapoints()

    def build_sensors(self):
        """
        Build Sensors in a Dict
        :return: 
        """
        self.sensors_dict = self.factory.build_objects_dict(self.factory.SENSOR, self.get_recipe_obj().get_sensor_id_list())
        for sensor in self.sensors_dict:
            self.sensor_processor.attach(sensor)
        return self.sensors_dict

    def build_appliances(self):
        """
        Build Appliances in a Dict
        :return: 
        """
        self.appliances_dict = self.factory.build_objects_dict(self.factory.APPLIANCE, self.get_recipe_obj().get_appliance_id_list())
        for appliance in self.appliances_dict:
            appliance.attach(self.appliance_processor)
        return self.appliances_dict

    def build_datapoints(self):
        """
        Build Datapoints in a Dict
        :return: 
        """
        return self.factory.build_objects_dict(self.factory.DATAPOINTS, self.get_recipe_obj().get_datapoints_id_list())

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
        pass

    def start_appliance_queue_processing(self):
        """
        Begins the Thread for processing the outgoing Appliance Readings
        :return: 
        """
        pass

    def stop_sensor_queue_processing(self):
        """
        Stops the Sensor Queue from receiving Sensor Readings
        :return: 
        """
        pass

    def stop_appliance_queue_processing(self):
        """
        Stops the Appliance Queue from receiving Appliance Readings
        :return: 
        """
        pass

    """
    Interactions
    """

    def start_sensors(self):
        """
        Start every sensor in the list of Sensors
        :return: 
        """
        pass

    def stop_sensors(self):
        """
        Stop every sensor in the list of Sensors
        :return: 
        """
        pass

    def add_sensor_reading_to_queue(self, reading, status_code=0):
        """
        Takes the reading and add it to the Sensor Reading Queue
        :param reading: A processed Sensor reading that is Recieved
        :return: 
        """
        self.sensor_queue.put_nowait(reading)

    def process_sensor_queue(self):
        sensor_reading = self.sensor_queue.get()
        datapoints_result_list = self.process_sensor_reading(sensor_reading)
        appliance_reading_list = self.process_datapoint_results_to_appliance(datapoints_result_list)
        for appliance_reading in appliance_reading_list:
            self.add_appliance_reading_to_queue(appliance_reading)

    def process_sensor_reading(self, sensor_reading):
        """
        Take a Sensor Reading from the Queue and build an output Reading based on the interaction with the Datapoints
        :return: The Output Reading(s) that will be sent to the Appliance Queue
        """

        # Check if Reading is of the right component type
        if not sensor_reading.get_component_id() == COMPONENT_TYPE_SENSOR:
            raise AttributeError

        # Get the relevant readings to be able to compare against a datapoints object
        recipe = self.get_recipe_obj()
        session = self.get_session_obj()
        sensor_id = sensor_reading.get_component_id()
        reading_timestamp = sensor_reading.get_reading_timestamp()
        time_elapsed = session.get_start_time() - reading_timestamp
        reading_value = sensor_reading.get_reading_value()

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

        recipe = self.get_recipe_obj()
        binder_list = recipe.get_appliance_datapoints_binding_ids()

        for binder in binder_list:
            if binder.get_datapoint_id() == datapoint_readings.get_component_id():
                binder_obj = BindDatapoitnsAppliances.get(binder.get_id())
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
        if not reading.get_component_id() == COMPONENT_TYPE_DATAPOINTS_APPLIANCE_BINDER:
            raise AttributeError

        self.appliance_queue.put_nowait(reading)


    def process_appliance_queue(self):
        """
        Take a Appliance Reading from the Queue and send to the relevant Appliance Objects
        :return: 
        """
        appliance_reading = self.appliance_queue.get()
        for appliance in self.appliances_dict:
            if appliance.get_id() == appliance_reading:
                appliance.recieve(appliance_reading)

