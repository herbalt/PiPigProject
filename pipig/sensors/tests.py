from flask import url_for
from wtforms import fields
from wtforms.validators import InputRequired

from test_helpers.test_base import BaseTestCase
from test_helpers.test_forms import FormTestCase

from pipig.sensors.forms import SensorsForm
from pipig.sensors.models import Sensor, SensorReading, SensorType, SensorUnits

from implementations import BaseSensor

class SensorFormTests(BaseTestCase, FormTestCase):

    def mock_form(self, name, sensor_type_id, interval_between_readings):
        return SensorsForm.populate(name=name, sensor_type_id=sensor_type_id, interval_between_readings=interval_between_readings)

    def mock_sensor(self):
        units = SensorUnits.create(code_name="TestUnits", display_units="T")
        type = SensorType.create(sensor_type="TestSensorType", sensor_units_id=1, minimum_refresh=0.0)
        sensor = Sensor.create(name="TestSensor", sensor_type_id=1, interval_between_readings=0.0)
        return sensor

    def test_add_field_type(self):
        self.form_class = SensorsForm

    def test_add_form_fields(self):
        self.form_class = SensorsForm
        self.assert_type('name', fields.StringField)
        self.assert_type('sensor_type_id', fields.IntegerField)
        self.assert_type('interval_between_readings', fields.FloatField)

    def test_add_validators(self):
        self.form_class = SensorsForm
        self.assert_has_validator('name', validator=InputRequired)
        self.assert_has_validator('sensor_type_id', validator=InputRequired())

    def test_add_form_validate_name(self):
        self.form_class = SensorsForm
        SensorType.create(sensor_type='Test Sensor Type', minimum_refresh=2.0)

        name_validate = self.mock_form("A valid form name", None, None)
        name_invalid = self.mock_form("", None, None)

        self.assertTrue(name_validate.validate_name(None), '%s does not validate correctly' % name_validate.name.data)
        self.assertFalse(name_invalid.validate_name(None), '%s does not validate correctly' % name_invalid.name.data)

    def test_add_form_validate_sensor_type_id(self):
        self.form_class = SensorsForm
        SensorType.create(sensor_type='Test Sensor Type', minimum_refresh=2.0)

        type_valid = self.mock_form("Valid Type", 1, None)
        type_invalid = self.mock_form("Invalid Type", 2, None)
        type_placeholder = self.mock_form("Placeholder Type", -1, None)

        self.assertTrue(type_valid.validate_sensor_type_id(None), '%s Sensor Type %d does not validate correctly'
                        % (type_valid.name, type_valid.sensor_type_id.data))
        self.assertFalse(type_invalid.validate_sensor_type_id(None), '%s Sensor Type %d does not validate correctly'
                         % (type_invalid.name, type_invalid.sensor_type_id.data))
        self.assertFalse(type_placeholder.validate_sensor_type_id(None), '%s Sensor Type %d does not validate correctly'
                         % (type_placeholder.name, type_placeholder.sensor_type_id.data))

    def test_add_from_validate_interval_between_readings(self):
        self.form_class = SensorsForm
        SensorType.create(sensor_type='Test Sensor Type', minimum_refresh=2.0)

        interval_valid = self.mock_form("Valid Interval", None, 2.1)
        interval_invalid = self.mock_form("Invalid Interval", None, 1.9)
        interval_placeholder = self.mock_form("Placeholder Interval", None, -1)


        self.assertTrue(interval_valid.validate_interval_between_readings(None), '%s Interval: %f does not validate correctly'
                        % (interval_valid.name, interval_valid.interval_between_readings.data))
        self.assertFalse(interval_invalid.validate_interval_between_readings(None), '%s Interval: %f does not validate correctly'
                        % (interval_invalid.name, interval_invalid.interval_between_readings.data))
        self.assertFalse(interval_placeholder.validate_interval_between_readings(None), '%s Interval: %f does not validate correctly'
                        % (interval_placeholder.name, interval_placeholder.interval_between_readings.data))


class SensorViewTests(BaseTestCase):

    def test_add_sensor(self):
        SensorType.create(sensor_type='Test Sensor Type')

        response = self.client.post(url_for('sensors.add_sensor'), data={'name': 'TestSensor', 'sensor_type_id': 1, 'interval_between_readings': 2.1})
        self.assertRedirects(response=response, location=url_for('sensors.sensor_list'))

        query = Sensor.query.filter_by(name='TestSensor').first()
        self.assertIsNotNone(query, "Sensor was not added to db")


class BaseSensorTests(BaseTestCase):
    class TestImplementedBaseSensor(BaseSensor):
        def take_reading(self):
            return None

    def mock_base_sensor(self):
        units = SensorUnits.create(code_name="TestUnits", display_units="T")
        type = SensorType.create(sensor_type="TestSensorType", sensor_units_id=1, minimum_refresh=0.0)
        sensor = Sensor.create(name="TestSensor", sensor_type_id=1, interval_between_readings=0.0)
        test_sensor = self.TestImplementedBaseSensor(sensor.get_id())
        return test_sensor

    def test_get_id(self):
        test_obj = self.mock_base_sensor()
        self.assertTrue(test_obj.get_id() == 1, "ID is %d instead of 1" % test_obj.get_id())

    def test_get_name(self):
        test_obj = self.mock_base_sensor()
        self.assertTrue(test_obj.get_name() == "TestSensor", "Name is %s instead of TestSensor" % test_obj.get_name())

    def test_get_interval_between_readings(self):
        test_obj = self.mock_base_sensor()
        self.assertTrue(test_obj.get_interval_between_readings() == 0.0, "Interval is %d instead of 0" % test_obj.get_interval_between_readings())

    def test_get_sensor_type_id(self):
        test_obj = self.mock_base_sensor()
        self.assertTrue(test_obj.get_sensor_type_id() == 1,
                        "Sensor Type ID is %d instead of 1" % test_obj.get_sensor_type_id())

    def test_get_minimum_refresh(self):
        test_obj = self.mock_base_sensor()
        self.assertTrue(test_obj.get_minimum_refresh() == 0.0,
                        "Sensor minimum refresh is %d instead of 0.0" % test_obj.get_minimum_refresh())

    def test_get_sensor_units(self):
        test_obj = self.mock_base_sensor()
        self.assertTrue(test_obj.get_sensor_units() == "T",
                        "Sensor Units is %s instead of T" % test_obj.get_sensor_units())

    def test_get_state(self):
        test_obj = self.mock_base_sensor()
        self.assertFalse(test_obj.get_state(),
                        "Sensor should init with a False State")

    def test_on_pre_execute(self):
        test_obj = self.mock_base_sensor()
        test_obj.on_pre_execute()
        self.assertTrue(test_obj.get_state() , "Sensor State should be True after Pre Execute")

    def test_do_in_background(self):
        self.assertTrue(False, "Not implemented")