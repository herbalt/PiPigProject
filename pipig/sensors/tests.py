from flask import url_for
from flask.ext.login import current_user
from wtforms import fields
from wtforms.validators import InputRequired, DataRequired


from test_helpers.test_base import BaseTestCase
from test_helpers.test_forms import FormTestCase

from pipig.sensors.forms import SensorsForm
from pipig.sensors.models import Sensor, SensorReading, SensorType

from pipig.data import db


class SensorFormTests(BaseTestCase, FormTestCase):

    def test_sensor_add_form(self):
        self.form_class = SensorsForm

        self.assert_type('name', fields.StringField)
        self.assert_type('sensor_type_id', fields.IntegerField)
        self.assert_type('interval_between_readings', fields.FloatField)

        # self.assert_has_validator('name', validator=InputRequired)
        # self.assert_has_validator('sensor_type_id', validator=InputRequired())
        # self.assert_has_validator('name', validator=InputRequired)
        # test= self.get_validator('name', DataRequired())

        SensorType.create(sensor_type='Test Sensor Type', minimum_refresh=2.0)

        valid_form = SensorsForm.populate(name='Valid', sensor_type_id=1, interval_between_readings=2.1)
        invalid_form = SensorsForm.populate(name='', sensor_type_id=2, interval_between_readings=2.1)
        invalid_form_interval = SensorsForm.populate(name='', sensor_type_id=1, interval_between_readings=1.9)
        placeholder_form = SensorsForm.populate(name='Placeholder', sensor_type_id=-1, interval_between_readings=-1)

        name_validate = valid_form.validate_name(None)
        name_invalid = invalid_form.validate_name(None)
        self.assertTrue(name_validate, '%s does not validate correctly' % valid_form.name.data)
        self.assertFalse(name_invalid, '%s does not validate correctly' % invalid_form.name.data)

        sensor_id_valid = valid_form.validate_sensor_type_id(None)
        sensor_id_invalid = invalid_form.validate_sensor_type_id(None)
        sensor_id_placeholder = placeholder_form.validate_sensor_type_id(None)
        self.assertTrue(sensor_id_valid, '%s Sensor Type %d does not validate correctly'
                        % (valid_form.name, valid_form.sensor_type_id.data))
        self.assertFalse(sensor_id_invalid, '%s Sensor Type %d does not validate correctly'
                         % (invalid_form.name, invalid_form.sensor_type_id.data))
        self.assertFalse(sensor_id_placeholder, '%s Sensor Type %d does not validate correctly'
                         % (placeholder_form.name, placeholder_form.sensor_type_id.data))

        interval_valid = valid_form.validate_interval_between_readings(None)
        interval_invalid = invalid_form_interval.validate_interval_between_readings(None)
        interval_placeholder = placeholder_form.validate_interval_between_readings(None)
        self.assertTrue(interval_valid, '%s Interval: %f does not validate correctly'
                        % (valid_form.name, valid_form.interval_between_readings.data))
        self.assertFalse(interval_invalid, '%s Interval: %f does not validate correctly'
                        % (invalid_form_interval.name, invalid_form_interval.interval_between_readings.data))
        self.assertFalse(interval_placeholder, '%s Interval: %f does not validate correctly'
                        % (placeholder_form.name, placeholder_form.interval_between_readings.data))


class SensorViewTests(BaseTestCase):

    def test_add_sensor(self):
        SensorType.create(sensor_type='Test Sensor Type')

        response = self.client.post(url_for('sensors.add_sensor'), data={'name': 'TestSensor', 'sensor_type_id': 1, 'interval_between_readings': 2.1})
        self.assertRedirects(response=response, location=url_for('sensors.sensor_list'))

        query = Sensor.query.filter_by(name='TestSensor').first()
        self.assertIsNotNone(query, "Sensor was not added to db")