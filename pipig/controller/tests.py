from test_helpers.test_base import BaseTestCase
from test_helpers.test_generics import run_equals_test, unwritten_test, run_object_equals_test
from controller.controller import Controller
from recipes.tests import MockRecipe
# from pi_pig.curing_sessions.tests import MockSession


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
        result = build_test_controller().get_curing_session_id()
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
        from pi_pig.curing_sessions.models import CuringSession
        expected = CuringSession(name="ControllerTest Session", start_time=0)
        expected.id = 1
        # expected = build_curing_session_model("ControllerTest Session")
        run_object_equals_test(self, result, expected, "Controller Session Object", "Failed to match equaility of attributes")
        # run_equals_test(self, result, expected, "Controller Session Object", "Failed to match equaility of attributes")


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




class ControllerQueueTests(BaseTestCase):
    """
    Queue Management
    """

    def mock(self):
        pass


class ControllerInteractionTests(BaseTestCase):
    """
    Interactions
    """

    def test_response_to_datapoint(self):
        obj = build_test_controller()
        self.helper_response_to_datapoint(obj, -1, 1, 1)

    def helper_response_to_datapoint(self, controller, diff_value, polarity, expected):
        result = controller.response_to_datapoint(diff_sensor_datapoint_value=diff_value, polarity=polarity)
        expected_result = expected
        run_equals_test(result=result, expected=expected_result, test_title="Response to Datapoint Reading", test_message="Incorrectly generated the wrong output value to send to an appliance_model", test_case=self)


# ________________________________________________________________
#
# Builders to use in Unit Tests
# ________________________________________________________________
from pi_pig.recipes.tests import build_recipe_model
from pi_pig.curing_sessions.tests import build_curing_session_model


def build_test_controller():
    recipe = build_recipe_model("ControllerTest")
    session = build_curing_session_model("ControllerTest Session")
    return TestController(recipe.get_id(), session.get_id())


class TestController(Controller):
    def __init__(self, recipe_id, curing_session_id=None):
        super(TestController, self).__init__(recipe_id, curing_session_id)


