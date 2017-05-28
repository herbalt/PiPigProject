import unittest


from appliances.tests import ApplianceModelTests, ApplianceObjectTests
# from bindings_datapoints.tests import BindDataPointsApplianceModelTests, BindDataPointsApplianceObjectTests, BindDataPointsSensorModelTests, BindDataPointsSensorObjectTests
# from binding_session.tests import BindSessionApplianceModelTests, BindSessionApplianceObjectTests, BindSessionSensorModelTests, BindSessionSensorObjectTests
from data_points.tests import DataPointsObjectTests, DataPointsObjectTestsDataPoint
from general.tests import ObjectTestsAsyncTask
# from gpio_pins.tests import GpioTests
from processors.tests import ProcessorObjectTests
from sensors.tests import SensorViewTests, SensorObjectTests, SensorReadingModelTests, SensorFormTests
from sessions.tests import SessionsModelTests
# from curing_session.tests import CuringSessionTests
# from users.tests import UserBlueprintTests, UserFormTests, UserViewsTests
from utilities.tests import UtilityTests
from recipes.tests import RecipesModelTests
from binders.tests import BindDataPointsSensorModelTests, BindDataPointsApplianceModelTests
from factories.tests import FactoryTests, FactorySensorTests, FactoryApplianceTests

from controller.tests import ControllerBuildTests, ControllerGetTests, ControllerInteractionTests, ControllerQueueTests
# from controller.tests import ControllerBuildTests
# from controller.tests import ControllerGetTests
# from controller.tests import ControllerInteractionTests
# from controller.tests import ControllerQueueTests

class TestSuite:
    def __init__(self):
        self.suite = unittest.TestSuite()

    def get_suite(self):
        self.appliances_tests()
        # self.bindings_datapoints_tests()
        # self.bindings_session_tests()
        self.data_point_tests()
        self.general_tests()
        self.gpio_tests()
        self.processor_tests()
        self.sensor_tests()
        # self.sessions_tests()
        self.binder_tests()
        self.recipe_tests()
        self.controller_tests()
        self.factory_tests()
        # self.users_tests()
        self.utilities_tests()
        return self.suite

    def appliances_tests(self):
        self.suite.addTest(unittest.makeSuite(ApplianceModelTests))
        self.suite.addTest(unittest.makeSuite(ApplianceObjectTests))
        return self.suite

    def bindings_datapoints_tests(self):
        # self.suite.addTest(unittest.makeSuite(BindDataPointsApplianceModelTests))
        # self.suite.addTest(unittest.makeSuite(BindDataPointsApplianceObjectTests))
        # self.suite.addTest(unittest.makeSuite(BindDataPointsSensorModelTests))
        # self.suite.addTest(unittest.makeSuite(BindDataPointsSensorObjectTests))
        return self.suite

    def bindings_session_tests(self):
        # self.suite.addTest(unittest.makeSuite(BindSessionApplianceModelTests))
        # self.suite.addTest(unittest.makeSuite(BindSessionApplianceObjectTests))
        # self.suite.addTest(unittest.makeSuite(BindSessionSensorModelTests))
        # self.suite.addTest(unittest.makeSuite(BindSessionSensorObjectTests))
        return self.suite

    def data_point_tests(self):
        self.suite.addTest(unittest.makeSuite(ApplianceObjectTests))
        self.suite.addTest(unittest.makeSuite(DataPointsObjectTestsDataPoint))
        return self.suite

    def general_tests(self):
        self.suite.addTest(unittest.makeSuite(ObjectTestsAsyncTask))
        return self.suite

    def gpio_tests(self):
        # self.suite.addTest(unittest.makeSuite(GpioTests))
        return self.suite

    def processor_tests(self):
        self.suite.addTest(unittest.makeSuite(ApplianceObjectTests))
        return self.suite

    def sensor_tests(self):
        self.suite.addTest(unittest.makeSuite(ApplianceObjectTests))
        self.suite.addTest(unittest.makeSuite(SensorFormTests))
        self.suite.addTest(unittest.makeSuite(ApplianceModelTests))
        self.suite.addTest(unittest.makeSuite(SensorViewTests))
        return self.suite

    def sessions_tests(self):
        self.suite.addTest(unittest.makeSuite(SessionsModelTests))
        # self.suite.addTest(unittest.makeSuite(CuringSessionTests))
        return self.suite

    def recipe_tests(self):
        self.suite.addTest(unittest.makeSuite(RecipesModelTests))
        # self.suite.addTest(unittest.makeSuite(CuringSessionTests))
        return self.suite

    def binder_tests(self):
        self.suite.addTest(unittest.makeSuite(BindDataPointsSensorModelTests))
        self.suite.addTest(unittest.makeSuite(BindDataPointsApplianceModelTests))
        return self.suite

    def controller_tests(self):

        # self.suite.addTest(unittest.makeSuite(ControllerInteractionTests))
        # self.suite.addTest(unittest.makeSuite(ControllerQueueTests))
        # self.suite.addTest(unittest.makeSuite(ControllerGetTests))
        # self.suite.addTest(unittest.makeSuite(ControllerBuildTests))

        return self.suite

    def factory_tests(self):
        self.suite.addTest(unittest.makeSuite(FactoryTests))
        self.suite.addTest(unittest.makeSuite(FactorySensorTests))
        self.suite.addTest(unittest.makeSuite(FactoryApplianceTests))
        return self.suite

    def users_tests(self):
        #self.suite.addTest(unittest.makeSuite(UserBlueprintTests))
        #self.suite.addTest(unittest.makeSuite(UserFormTests))
        #self.suite.addTest(unittest.makeSuite(UserViewsTests))
        return self.suite

    def utilities_tests(self):
        self.suite.addTest(unittest.makeSuite(UtilityTests))
        return self.suite

runner = unittest.TextTestRunner()
runner.run(TestSuite().get_suite())