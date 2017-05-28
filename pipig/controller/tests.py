from test_helpers.test_base import BaseTestCase
from test_helpers.test_generics import run_equals_test, unwritten_test, run_object_equals_test
from pipig.controller.controller import Controller
from pipig.recipes.tests import MockRecipe
# from pipig.sessions.tests import MockSession


# ________________________________________________________________
#
# Unit Tests
# ________________________________________________________________
class ControllerGetTests(BaseTestCase):
    def test_get_recipe_id(self):
        result = build_test_controller().get_recipe_id()
        expected = 1
        run_equals_test(self, result, expected, "Controller Recipe", "Failed to match IDs")

    def test_get_session_id(self):
        result = build_test_controller().get_session_id()
        expected = 1
        run_equals_test(self, result, expected, "Controller Session", "Failed to match IDs")

    def test_get_recipe_obj(self):
        result = build_test_controller().get_recipe_obj()
        expected = MockRecipe("ControllerTestRecipeModel")
        run_object_equals_test(self, result, expected, "Controller Recipe Object", "Failed to match equaility of attributes")

    def test_get_session_obj(self):
        result = build_test_controller().get_session_obj()
        # expected = MockSession("ControllerTest SessionSessionModel", 1, 0)
        # TODO REQUIRES A SEESSION OBJECT TO RUN TEST CORRECTLY
        expected = "REQUIRES A SESSION OBJECT"
        run_equals_test(self, result, expected, "Controller Session Object", "Failed to match equaility of attributes")


class ControllerBuildTests(BaseTestCase):
    """
    Build Methods
    """

    def test_build_controller(self):
        """
        Main method to call from init to construct the environment
        
        This should test if every required method is called in the correct order if necessary.
        Use a Mock Controller Object that returns True for the required methods
        
        :return: 
        """
        class MockBuildController(Controller):
            def __init__(self, recipe_id):
                super(MockBuildController, self).__init__(recipe_id)

            def build_controller(self):
                return True

            def build_objects(self):
                return True

            def bind_sensor_objects(self):
                return True

            def bind_appliance_objects(self):
                return True

        mock = MockBuildController(1)

        build = mock.build_objects()
        bind_sensor = mock.bind_sensor_objects()
        bind_appliance = mock.bind_appliance_objects()

        run_equals_test(self, [build, bind_sensor, bind_appliance], [True, True, True], "test_build_controller",
                        "Object Method Calls were trigged incorrectly. Should be BUILD, BIND_SENSOR, BIND_APPLIANCE")

    def test_build_objects(self):
        """
        Build all Sensors, Datapoints and Appliances
        :return: 
        """

        class MockBuildObjectsController(Controller):
            def __init__(self, recipe_id):
                super(MockBuildObjectsController, self).__init__(recipe_id)

            def build_controller(self):
                return True

            def build_sensors(self):
                return True

            def build_appliances(self):
                return True

            def build_datapoints(self):
                return True

        mock = MockBuildObjectsController(1)

        build_sensors = mock.build_sensors()
        build_appliances = mock.build_appliances()
        build_datapoints = mock.build_datapoints()

        run_equals_test(self, [build_sensors, build_appliances, build_datapoints], [True, True, True], "objects",
                        "Object Method Calls were trigged incorrectly. Should be SENSORS, APPLIANCES, DATAPOINTS")

    def test_build_sensors(self):
        """
        Builds all Sensors in a List
        :return: 
        """
        unwritten_test(self)

        # recipe = MockRecipe("ControllerBuildSensors")
        # sensor_ids = recipe.get_sensor_ids()

    def test_build_appliances(self):
        """
        Builds all Appliances in a List
        :return: 
        """
        unwritten_test(self)

    def test_build_datapoints(self):
        """
        Builds all Datapoints in a List
        :return: 
        """
        unwritten_test(self)

    def test_bind_sensor_objects(self):
        """
        Bind Sensor Objects to Controller
        :return: 
        """
        unwritten_test(self)

    def test_bind_appliance_objects(self):
        """
        Bind Controller to Appliances
        :return: 
        """
        unwritten_test(self)


class ControllerQueueTests(BaseTestCase):
    """
    Queue Management
    """

    def test_start_sensor_queue_processing(self):
        """
        Begins the Thread for processing the incoming Sensor Readings
        :return: 
        """
        unwritten_test(self)

    def test_start_appliance_queue_processing(self):
        """
        Begins the Thread for processing the outgoing Appliance Readings
        :return: 
        """
        unwritten_test(self)

    def test_stop_sensor_queue_processing(self):
        """
        Stops the Sensor Queue from receiving Sensor Readings
        :return: 
        """
        unwritten_test(self)

    def test_stop_appliance_queue_processing(self):
        """
        Stops the Appliance Queue from receiving Appliance Readings
        :return: 
        """
        unwritten_test(self)


class ControllerInteractionTests(BaseTestCase):
    """
    Interactions
    """

    def test_start_sensors(self):
        """
        Start every sensor in the list of Sensors
        :return: 
        """
        unwritten_test(self)

    def test_stop_sensors(self):
        """
        Stop every sensor in the list of Sensors
        :return: 
        """
        unwritten_test(self)

    def test_add_sensor_reading_to_queue(self, reading, status_code=0):
        """
        Takes the reading and add it to the Sensor Reading Queue
        :param reading: A processed Sensor reading that is Recieved
        :return: 
        """
        unwritten_test(self)

    def test_process_sensor_reading(self):
        """
        Take a Sensor Reading from the Queue and build an output Reading based on the interaction with the Datapoints
        :return: The Output Reading(s) that will be sent to the Appliance Queue
        """
        unwritten_test(self)

    def test_add_appliance_reading_to_queue(self, reading):
        """
        Add the Appliance Reading to the Appliance Queue
        :param reading: A output reading that is to be processed by the Appliances
        :return: 
        """
        unwritten_test(self)

    def test_process_appliance_queue(self):
        """
        Take a Appliance Reading from the Queue and send to the relevant Appliance Objects
        :return: 
        """
        unwritten_test(self)


# ________________________________________________________________
#
# Builders to use in Unit Tests
# ________________________________________________________________
from pipig.recipes.tests import build_recipe_model
from pipig.sessions.tests import build_session_model


def build_test_controller():
    recipe = build_recipe_model("ControllerTest")
    session = build_session_model("ControllerTest Session")
    return TestController(recipe.get_id(), session.get_id())


class TestController(Controller):
    def __init__(self, recipe_id, session_id=None):
        super(TestController, self).__init__(recipe_id, session_id)


