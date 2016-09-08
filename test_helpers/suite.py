import unittest

from appliances.tests import ApplianceTests
from bindings.tests import BindingTests
from data_points.tests import DataPointsTests
from general.tests import AsyncTaskTests
from gpio_pins.tests import GpioTests
from processors.tests import ProcessorsTests
from sensors.tests import SensorViewTests, BaseSensorTests, SensorReadingsTests, SensorFormTests
from sessions.tests import SessionTests
from users.tests import UserBlueprintTests, UserFormTests, UserViewsTests
from utilities.tests import UtilityTests


class TestSuite():
    def __init__(self):
        self.suite = unittest.TestSuite()

    def get_suite(self):
        self.appliances_tests()
        self.bindings_tests()
        self.data_point_tests()
        self.general_tests()
        self.gpio_tests()
        self.processor_tests()
        self.sensor_tests()
        self.sessions_tests()
        self.users_tests()
        self.utilities_tests()
        return self.suite

    def appliances_tests(self):
        self.suite.addTest(unittest.makeSuite(ApplianceTests))
        return self.suite

    def bindings_tests(self):
        self.suite.addTest(unittest.makeSuite(BindingTests))
        return self.suite

    def data_point_tests(self):
        self.suite.addTest(unittest.makeSuite(DataPointsTests))
        return self.suite

    def general_tests(self):
        self.suite.addTest(unittest.makeSuite(AsyncTaskTests))
        return self.suite

    def gpio_tests(self):
        self.suite.addTest(unittest.makeSuite(GpioTests))
        return self.suite

    def processor_tests(self):
        self.suite.addTest(unittest.makeSuite(ProcessorsTests))
        return self.suite

    def sensor_tests(self):
        self.suite.addTest(unittest.makeSuite(BaseSensorTests))
        self.suite.addTest(unittest.makeSuite(SensorFormTests))
        self.suite.addTest(unittest.makeSuite(SensorReadingsTests))
        self.suite.addTest(unittest.makeSuite(SensorViewTests))
        return self.suite

    def sessions_tests(self):
        self.suite.addTest(unittest.makeSuite(SessionTests))
        return self.suite

    def users_tests(self):
        self.suite.addTest(unittest.makeSuite(UserBlueprintTests))
        self.suite.addTest(unittest.makeSuite(UserFormTests))
        self.suite.addTest(unittest.makeSuite(UserViewsTests))
        return self.suite

    def utilities_tests(self):
        self.suite.addTest(unittest.makeSuite(UtilityTests))
        return self.suite

runner = unittest.TextTestRunner()
runner.run(TestSuite().get_suite())