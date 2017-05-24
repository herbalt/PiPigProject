from pipig.sessions.models import Session
from pipig.recipes.models import Recipe
from pipig.general.patterns import Subject, Observer


class Controller(Observer):
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
        pass

    def bind_sensor_objects(self):
        """
        Bind Sensor Objects to Controller
        :return: 
        """
        pass

    def bind_appliance_objects(self):
        """
        Bind Controller to Appliances
        :return: 
        """
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
        pass

    def process_sensor_reading(self):
        """
        Take a Sensor Reading from the Queue and build an output Reading based on the interaction with the Datapoints
        :return: The Output Reading(s) that will be sent to the Appliance Queue
        """
        pass

    def add_appliance_reading_to_queue(self, reading):
        """
        Add the Appliance Reading to the Appliance Queue
        :param reading: A output reading that is to be processed by the Appliances
        :return: 
        """
        pass

    def process_appliance_queue(self):
        """
        Take a Appliance Reading from the Queue and send to the relevant Appliance Objects
        :return: 
        """
        pass
