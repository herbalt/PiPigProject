from flask import url_for
from flask.ext.login import current_user
from wtforms import fields
from wtforms.validators import InputRequired


from test_helpers.test_base import BaseTestCase
from test_helpers.test_forms import FormTestCase

from pipig.sensors.forms import SensorsForm
from pipig.sensors.models import Sensor, SensorReading, SensorType

class SensorFormTests(BaseTestCase, FormTestCase):

    def test_sensor_add_form(self):
        self.form_class = SensorsForm

        self.assert_type('name', fields.StringField)
        self.assert_type('sensor_factory_id', fields.IntegerField)
        self.assert_type('interval_between_readings', fields.FloatField)

        # self.assert_has_validator('name', validator=InputRequired)
        # self.assert_has_validator('sensor_factory_id', validator=InputRequired)

        test_form = SensorsForm.populate(name='Test', sensor_factory_id='1', interval_between_readings='2.1')

        name_validate = test_form.validate_name(None)
        self.assertTrue(name_validate, 'Name: %s does not validate' % test_form.name)

        sensor_id_validate = test_form.validate_factory_id(None)
        self.assertTrue(sensor_id_validate, 'Sensor ID: %d does not validate' % test_form.sensor_factory_id)

        interval_validate = test_form.validate_name(None)
        self.assertTrue(interval_validate, 'Interval: %f does not validate' % test_form.interval_between_readings)


