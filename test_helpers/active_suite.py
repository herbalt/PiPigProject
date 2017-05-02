import unittest

from appliances.tests import ApplianceModelTests, ApplianceObjectTests
from sensors.tests import SensorObjectTests, SensorFormTests, SensorModelTests, SensorReadingModelTests, SensorViewTests
from data_points.tests import DataPointsObjectTests, DataPointsObjectTestsDataPoint
from sessions.tests import SessionsModelTests
from processors.tests import ProcessorObjectTests
from general.tests import ObjectTestsAsyncTask
from binding_session.tests import BindSessionSensorModelTests, BindSessionSensorObjectTests, BindSessionApplianceModelTests, BindSessionApplianceObjectTests
from bindings_datapoints.tests import BindDataPointsApplianceModelTests, BindDataPointsApplianceObjectTests, BindDataPointsSensorModelTests, BindDataPointsSensorObjectTests

from utilities.tests import UtilityTests



class ActiveTestSuite():
    def __init__(self):
        self.suite = unittest.TestSuite()

    def get_suite(self):
        self.appliances_tests()
        self.binding_sessions_tests()
        self.binding_datapoints_tests()
        self.data_point_tests()
        self.general_tests()
        # self.gpio_tests()
        self.processor_tests()
        self.sensor_tests()

        self.sessions_tests()
        # self.curing_session_tests()
        # self.users_tests()
        self.utilities_tests()
        return self.suite

    def appliances_tests(self):
        self.suite.addTest(unittest.makeSuite(ApplianceModelTests))
        self.suite.addTest(unittest.makeSuite(ApplianceObjectTests))
        return self.suite

    def binding_sessions_tests(self):
        self.suite.addTest(unittest.makeSuite(BindSessionSensorModelTests))
        self.suite.addTest(unittest.makeSuite(BindSessionSensorObjectTests))
        self.suite.addTest(unittest.makeSuite(BindSessionApplianceModelTests))
        self.suite.addTest(unittest.makeSuite(BindSessionApplianceObjectTests))
        return self.suite

    def binding_datapoints_tests(self):
        self.suite.addTest(unittest.makeSuite(BindDataPointsApplianceModelTests))
        self.suite.addTest(unittest.makeSuite(BindDataPointsApplianceObjectTests))
        self.suite.addTest(unittest.makeSuite(BindDataPointsSensorModelTests))
        self.suite.addTest(unittest.makeSuite(BindDataPointsSensorObjectTests))
        return self.suite

    def data_point_tests(self):
        self.suite.addTest(unittest.makeSuite(DataPointsObjectTests))
        self.suite.addTest(unittest.makeSuite(DataPointsObjectTestsDataPoint))
        return self.suite

    def general_tests(self):
        self.suite.addTest(unittest.makeSuite(ObjectTestsAsyncTask))
        return self.suite

    def gpio_tests(self):
        # self.suite.addTest(unittest.makeSuite(GpioTests))
        return self.suite

    def processor_tests(self):
        self.suite.addTest(unittest.makeSuite(ProcessorObjectTests))
        return self.suite

    def sensor_tests(self):
        self.suite.addTest(unittest.makeSuite(SensorObjectTests))
        self.suite.addTest(unittest.makeSuite(SensorFormTests))
        self.suite.addTest(unittest.makeSuite(SensorModelTests))
        self.suite.addTest(unittest.makeSuite(SensorReadingModelTests))
        self.suite.addTest(unittest.makeSuite(SensorViewTests))
        return self.suite

    def sessions_tests(self):
        self.suite.addTest(unittest.makeSuite(SessionsModelTests))
        return self.suite

    def curing_session_tests(self):
        # self.suite.addTest(unittest.makeSuite(CuringSessionTests))
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
# with app.app_context():
runner.run(ActiveTestSuite().get_suite())
# runner.run(ActiveTestSuite().get_suite())