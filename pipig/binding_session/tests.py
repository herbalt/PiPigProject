from appliances.tests import build_appliance_model
from binding_session.session_binding import SessionSensorBinder, SessionApplianceBinder
from test_helpers.test_base import BaseTestCase
from test_helpers.test_forms import FormTestCase
from test_helpers.test_generics import unwritten_test

from binding_session.models import BindSessionAppliances, BindSessionsSensors

from sessions.models import Session
from sessions.tests import build_session_model

from sensors.models import Sensor, SensorType
from sensors.tests import build_sensor_model

from appliances.models import Appliance, ApplianceType

# ________________________________________________________________
#
# Unit Tests
# ________________________________________________________________


class BindSessionSensorModelTests(BaseTestCase):
    def model_session_sensor(self):

        result = BindSessionsSensors.create(session_id=1, sensor_id=1)
        return result

    def test_get_id(self):
        result = build_session_sensor_model("Test", "T", 0.005, 0.02, None)
        self.assertTrue(result.get_id() == 1, "%s should create an ID of 1, however was an ID of %d" % (str(result), result.get_id()))


    def test_get_session_id(self):
        result = build_session_sensor_model("Test", "T", 0.005, 0.02, None)
        self.assertTrue(result.get_session_id() == 1,
                        "%s should create a Session ID of 1, however was a Session ID of %d" % (str(result), result.get_session_id()))

    def test_get_sensor_id(self):
        result = build_session_sensor_model("Test", "T", 0.005, 0.02, None)
        self.assertTrue(result.get_sensor_id() == 1,
                        "%s should create a Sensor ID of 1, however was a Sensor ID of %d" % (str(result), result.get_sensor_id()))


class BindSessionSensorObjectTests(BaseTestCase):

    def test_get_id(self):
        result = build_session_sensor_object("Test", "T", 0.005, 0.02, None)
        self.assertIsNotNone(result, "SessionSensor should not be None after build")
        self.assertTrue(result.get_id() == 1,
                        "%s should create an ID of 1, however was an ID of %d" % (str(result), result.get_id()))


    def test_get_session_id(self):
        result = build_session_sensor_object("Test", "T", 0.005, 0.02, None)
        self.assertIsNotNone(result, "SessionSensor should not be None after build")
        self.assertTrue(result.get_session_id() == 1,
                        "%s should create an Session ID of 1, however was an Session ID of %d" % (str(result), result.get_session_id()))

    def test_get_sensor_id(self):
        result = build_session_sensor_object("Test", "T", 0.005, 0.02, None)
        self.assertIsNotNone(result, "SessionSensor should not be None after build")
        self.assertTrue(result.get_sensor_id() == 1,
                        "%s should create an Sensor ID of 1, however was an Sensor ID of %d" % (str(result), result.get_sensor_id()))


class BindSessionApplianceModelTests(BaseTestCase):
    def test_get_id(self):
        result = build_session_appliance_model("Test", "T", None)
        self.assertTrue(result.get_id() == 1, "%s should create a ID of 1, however was a ID of %d" % (str(result), result.get_id()))

    def test_get_session_id(self):
        result = build_session_appliance_model("Test", "T", None)
        self.assertTrue(result.get_session_id() == 1,
                        "%s should create a Session ID of 1, however was a Session ID of %d" % (str(result), result.get_session_id()))

    def test_get_appliance_id(self):
        result = build_session_appliance_model("Test", "T", None)
        self.assertTrue(result.get_appliance_id() == 1,
                        "%s should create a Appliance ID of 1, however was a Appliance ID of %d" % (str(result), result.get_appliance_id()))


class BindSessionApplianceObjectTests(BaseTestCase):

    def test_get_id(self):
        result = build_session_appliance_object("Test", "T", None)
        self.assertIsNotNone(result, "SessionAppliance should not be None after build")
        self.assertTrue(result.get_id() == 1,
                        "%s should create an ID of 1, however was an ID of %d" % (str(result), result.get_id()))

    def test_get_session_id(self):
        result = build_session_appliance_object("Test", "T", None)
        self.assertIsNotNone(result, "SessionAppliance should not be None after build")
        self.assertTrue(result.get_session_id() == 1,
                        "%s should create a Session ID of 1, however was a Session ID of %d" % (str(result), result.get_session_id()))

    def test_get_appliance_id(self):
        result = build_session_appliance_object("Test", "T", None)
        self.assertIsNotNone(result, "SessionAppliance should not be None after build")
        self.assertTrue(result.get_appliance_id() == 1,
                        "%s should create a Appliance ID of 1, however was a Appliance ID of %d" % (str(result), result.get_appliance_id()))

# ________________________________________________________________
#
# Builders to use in Unit Tests
# ________________________________________________________________

def build_session_sensor_model(base_name, display_units, minimum_refresh, interval_between_readings, gpio_pin_number=None):
    session_id = build_session_model(base_name)
    sensor_id = build_sensor_model(base_name, display_units, minimum_refresh, interval_between_readings, gpio_pin_number)
    session_sensor = BindSessionsSensors.create(session_id=session_id.get_id(), sensor_id=sensor_id.get_id())
    return session_sensor


def build_session_sensor_object(base_name, display_units, minimum_refresh, interval_between_readings, gpio_pin_number=None):
    session_sensor = build_session_sensor_model(base_name, display_units, minimum_refresh, interval_between_readings, gpio_pin_number)
    result = SessionSensorBinder(session_sensor.get_id())
    return result


def build_session_appliance_model(base_name, display_units, gpio_pin_number=None):
    session_id = build_session_model(base_name)
    appliance_id = build_appliance_model(base_name, display_units, gpio_pin_number)
    session_appliance = BindSessionAppliances.create(session_id=session_id.get_id(), appliance_id=appliance_id.get_id())
    return session_appliance

def build_session_appliance_object(base_name, display_units, gpio_pin_number=None):
    session_appliance = build_session_appliance_model(base_name, display_units, gpio_pin_number)
    result = SessionApplianceBinder(session_appliance.get_id())
    return result

# ________________________________________________________________
#
# Objects to use in Unit Tests
# ________________________________________________________________