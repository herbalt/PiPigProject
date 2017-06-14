from flask import url_for
from wtforms import fields
from wtforms.validators import InputRequired

from general.patterns import Observer
from generics.constants import COMPONENT_TYPE_SENSOR
from test_helpers.test_base import BaseTestCase
from test_helpers.test_forms import FormTestCase

from pipig.sensors.forms import SensorsForm
from pipig.sensors.models import Sensor, SensorType
from generics.models import GenericReading, GenericUnits

from sensor import BaseSensor
from pi_gpio.models import GpioPin
from time import sleep

from test_helpers.test_generics import unwritten_test

#________________________________________________________________
#
# Unit Tests
#________________________________________________________________
class SensorFormTests(BaseTestCase, FormTestCase):

    def mock_form(self, name, sensor_type_id, interval_between_readings):
        return SensorsForm.populate(name=name, type_id=sensor_type_id, interval_between_readings=interval_between_readings)

    def mock_sensor(self):
        units = GenericUnits.create(code_name="TestUnits", display_units="T")
        type = SensorType.create(sensor_type="TestSensorType", sensor_units_id=1, minimum_refresh=0.01)
        sensor = Sensor.create(name="TestSensor", sensor_type_id=1, interval_between_readings=0.02)
        return sensor

    def test_add_field_type(self):
        self.form_class = SensorsForm

    def test_add_form_fields(self):
        self.form_class = SensorsForm
        self.assert_type('name', fields.StringField)
        self.assert_type('type_id', fields.IntegerField)
        self.assert_type('interval_between_readings', fields.FloatField)

    def test_add_validators(self):
        self.form_class = SensorsForm

        self.assert_has_validator('name', validator=InputRequired)
        self.assert_has_validator('type_id', validator=InputRequired)

    def test_add_form_validate_name(self):
        self.form_class = SensorsForm
        SensorType.create(type_name='Test Sensor Type', minimum_refresh=2.0)

        name_validate = self.mock_form("A valid form name", None, None)
        name_invalid = self.mock_form("", None, None)

        self.assertTrue(name_validate.validate_name(None), '%s does not validate correctly' % name_validate.name.data)
        self.assertFalse(name_invalid.validate_name(None), '%s does not validate correctly' % name_invalid.name.data)

    def test_add_form_validate_sensor_type_id(self):
        self.form_class = SensorsForm
        SensorType.create(type_name='Test Sensor Type', minimum_refresh=2.0)

        type_valid = self.mock_form("Valid Type", 1, None)
        type_invalid = self.mock_form("Invalid Type", 2, None)
        type_placeholder = self.mock_form("Placeholder Type", -1, None)

        self.assertTrue(type_valid.validate_type_id(None), '%s Sensor Type %d does not validate correctly'
                        % (type_valid.name, type_valid.type_id.data))
        self.assertFalse(type_invalid.validate_type_id(None), '%s Sensor Type %d does not validate correctly'
                         % (type_invalid.name, type_invalid.type_id.data))
        self.assertFalse(type_placeholder.validate_type_id(None), '%s Sensor Type %d does not validate correctly'
                         % (type_placeholder.name, type_placeholder.type_id.data))

    def test_add_from_validate_interval_between_readings(self):
        self.form_class = SensorsForm
        sensor_type = SensorType.create(type_name='Test Sensor Type', minimum_refresh=2.0)

        interval_valid = self.mock_form("Valid Interval", 1, 2.1)
        interval_invalid = self.mock_form("Invalid Interval", 1, 0.001)
        interval_placeholder = self.mock_form("Placeholder Interval", 1, -1)


        self.assertTrue(interval_valid.validate_interval_between_readings(None), '%s Interval: %f does not validate correctly'
                        % (interval_valid.name, interval_valid.interval_between_readings.data))
        self.assertFalse(interval_invalid.validate_interval_between_readings(None), '%s Interval: %f does not validate correctly'
                        % (interval_invalid.name, interval_invalid.interval_between_readings.data))
        self.assertFalse(interval_placeholder.validate_interval_between_readings(None), '%s Interval: %f does not validate correctly'
                        % (interval_placeholder.name, interval_placeholder.interval_between_readings.data))


class SensorViewTests(BaseTestCase):

    def test_add_sensor(self):
        SensorType.create(type_name='Test Sensor Type')

        response = self.client.post(url_for('sensors.add_sensor'), data={'name': 'TestSensor', 'type_id': 1, 'interval_between_readings': 2.1})
        self.assertRedirects(response=response, location=url_for('sensors.sensor_list'))

        query = Sensor.query.filter_by(name='TestSensor').first()
        self.assertIsNotNone(query, "Sensor was not added to db")


def helper_populate_sensor_readings(sensor_id, sensorvalue_timestamp_tuple_list):
    for reading in sensorvalue_timestamp_tuple_list:
        GenericReading.create(component_id=sensor_id, component_type_id=COMPONENT_TYPE_SENSOR,
                              reading_value=reading[0], reading_timestamp=reading[1])

class SensorModelTests(BaseTestCase):
    def test_get_readings(self):
        obj = build_sensor_model("Test", "T", 0.005, 0.02, None)
        sensor_tuple_list = [(2.0, 0.0), (10.0, 0.1), (18.0, 0.2), (28.0, 0.4)]
        helper_populate_sensor_readings(obj.get_id(), sensor_tuple_list)

        result = obj.get_readings()
        result_tuple_list = []
        for reading in result:
            result_tuple_list.append((reading.get_value(), reading.get_timestamp()))

        self.assertListEqual(sensor_tuple_list, result_tuple_list, "Tuple lists shoudl be the same \nExpected\n%s\nResult\n%s" % (str(sensor_tuple_list), str(result_tuple_list)))


    def helper_get_reading_at_time(self, obj, expected, reading_time):
        point = obj.get_reading_at_time(reading_time)
        result_value = point.get_value()
        self.assertTrue(result_value == expected, "%s should have a result of %d, however is %d" % (str(obj), expected, result_value))

    def test_get_reading_at_time(self):
        obj = build_sensor_model("Test", "T", 0.005, 0.02, None)
        sensor_tuple_list = [(2.0, 0.0), (10.0, 0.1), (18.0, 0.2), (28.0, 0.4)]
        helper_populate_sensor_readings(obj.get_id(), sensor_tuple_list)

        self.helper_get_reading_at_time(obj, 2.0, 0.0)
        self.helper_get_reading_at_time(obj, 10.0, 0.1)

    def test_get_reading_at_time_irregular_values(self):
        obj = build_sensor_model("Test", "T", 0.005, 0.02, None)
        sensor_tuple_list = [(2.0, 0.0), (10.0, 0.1), (18.0, 0.2), (28.0, 0.4)]
        helper_populate_sensor_readings(obj.get_id(), sensor_tuple_list)

        self.helper_get_reading_at_time(obj, 6.0, 0.005)
        self.helper_get_reading_at_time(obj, 23.0, 0.3)

        self.helper_get_reading_at_time(obj, 28.0, 0.5)

class SensorReadingModelTests(BaseTestCase):

    def test_can_build(self):
        result = GenericReading(1, COMPONENT_TYPE_SENSOR, 1.0, 1.2)
        self.assertTrue(type(result) == GenericReading, "Type %s" % type(result))

    def test_can_commit_to_db(self):
        result = GenericReading.create(component_id=1, component_type_id=COMPONENT_TYPE_SENSOR, reading_value=1.9, reading_timestamp=1.2)
        self.assertTrue(type(result) == GenericReading, "Type %s" % type(result))



class SensorObjectTests(BaseTestCase):

    def mock_base_sensor(self):
        return build_sensor_object("Test", "T", 0.005, 0.02, None)

    def mock_base_sensor_with_gpio_pin(self):
        return build_sensor_object("TestGpio", "T", 0.005, 0.02, 1)

    def test_get_id(self):
        test_obj = self.mock_base_sensor()
        self.assertTrue(test_obj.get_id() == 1, "ID is %d instead of 1" % test_obj.get_id())

    def test_get_name(self):
        test_obj = self.mock_base_sensor()
        self.assertTrue(test_obj.get_name() == "TestSensor", "Name is %s instead of TestSensor" % test_obj.get_name())

    def test_get_interval_between_readings(self):
        test_obj = self.mock_base_sensor()
        self.assertTrue(test_obj.get_interval_between_readings() == 0.02, "Interval is %d instead of 0" % test_obj.get_interval_between_readings())

    def test_get_sensor_type_id(self):
        test_obj = self.mock_base_sensor()
        self.assertTrue(test_obj.get_type_id() == 1,
                        "Sensor Type ID is %d instead of 1" % test_obj.get_type_id())

    def test_get_minimum_refresh(self):
        test_obj = self.mock_base_sensor()
        min = test_obj.get_minimum_refresh()
        self.assertTrue(test_obj.get_minimum_refresh() == 0.005,
                        "Sensor minimum refresh is %f instead of 0.005" % test_obj.get_minimum_refresh())

    def test_get_sensor_units(self):
        test_obj = self.mock_base_sensor()
        self.assertTrue(test_obj.get_units() == "T",
                        "Sensor Units is %s instead of T" % test_obj.get_units())

    def test_get_state(self):
        test_obj = self.mock_base_sensor()
        self.assertFalse(test_obj.get_state(),
                        "Sensor should init with a False State")

    def test_get_gpio_pin(self):
        test_obj = self.mock_base_sensor_with_gpio_pin()
        self.assertTrue(test_obj.get_gpio_pin() == 1)

    def test_get_gpio_pin_defaults_none(self):
        test_obj = self.mock_base_sensor()
        self.assertIsNone(test_obj.get_gpio_pin())

    def test_on_pre_execute(self):
        test_obj = self.mock_base_sensor()
        test_obj.on_pre_execute()
        self.assertTrue(test_obj.get_state() , "Sensor State should be True after Pre Execute")

    def test_async_sensor(self):
        test_obj = self.mock_base_sensor()
        test_observer = ObjectObserver()
        test_obj.attach(test_observer)


        fake = test_obj.get_interval_between_readings()


        test_obj.execute_operation()
        sleep(0.1)
        test_obj.cancel_operation()
        sleep(0.1)

        results = test_observer.get_results()
        expected_results = [(None, 1), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (None, 4)]

        message = "Async Sensor not working correctly.\nis: \n%s \nshould be:\n%s " % (str(results), str(expected_results))
        self.assertTrue(len(results) > 5, message)
        self.assertTrue(results[0] == expected_results[0], message)
        self.assertTrue(results[-1] == expected_results[-1], message)





#________________________________________________________________
#
# Builds to use in Tests
#________________________________________________________________

def build_sensor_model(base_name, display_units, minimum_refresh, interval_between_readings, gpio_pin_number=None):
    units = GenericUnits.create(code_name="%sUnits" % base_name, display_units=display_units)
    type = SensorType.create(type_name="%sSensorType" % base_name, units_id=units.get_id(),
                             minimum_refresh=minimum_refresh)
    if gpio_pin_number is not None:
        gpio_id = GpioPin.create(pin_number=gpio_pin_number, pin_name="%sPin%d" % (base_name, gpio_pin_number)).get_id()
    else:
        gpio_id = None
    sensor = Sensor.create(name="%sSensor" % base_name, type_id=type.get_id(),
                           interval_between_readings=interval_between_readings, gpio_pin_id=gpio_id)
    return sensor


def build_sensor_object(base_name, display_units, minimum_refresh, interval_between_readings, gpio_pin_number=None):
    sensor = build_sensor_model(base_name, display_units, minimum_refresh, interval_between_readings, gpio_pin_number)
    test_sensor = ObjectBaseSensor(sensor.get_id())
    return test_sensor


#________________________________________________________________
#
# Objects to use in Tests
#________________________________________________________________


class ObjectBaseSensor(BaseSensor):
    def __init__(self, sensor_id):
        BaseSensor.__init__(self, sensor_id=sensor_id)
        self.counter = 0

    def take_reading(self):
        self.counter += 1
        return self.counter


class ObjectObserver(Observer):
    def __init__(self):
        Observer.__init__(self)
        self.results = []

    def receive(self, result, status_code=0):
        if result is not None:
            result = result.get_value()
        self.results.append((result, status_code))

    def get_results(self):
        return self.results
