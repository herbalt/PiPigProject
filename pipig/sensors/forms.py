from flask_wtf import Form
from wtforms import fields
from wtforms.validators import InputRequired, ValidationError

import pipig.sensors.models as sensors


class SensorsForm(Form):
    name = fields.StringField(InputRequired())
    sensor_factory_id = fields.IntegerField(InputRequired())
    interval_between_readings = fields.FloatField()

    @staticmethod
    def populate(name='', sensor_factory_id=-1, interval_between_readings=-1):
        obj = SensorsForm()
        obj.name = name
        obj.sensor_factory_id = sensor_factory_id
        obj.interval_between_readings = interval_between_readings
        return obj

    def validate_name(form, field):
        name = sensors.Sensor.query.filter_by(name=form.name).first()
        if name == '':
            return False
        return True

    def validate_factory_id(form, field):
        factory_id = sensors.Sensor.query.filter_by(sensor_factory_id=form.sensor_factory_id.data).first()
        if factory_id < 0:
            return False
        return True

    def validate_interval_between_readings(form, field):
        i_b_r = sensors.Sensor.query.filter_by(interval_between_readings=form.interval_between_readings.data).first()
        if i_b_r < 0:
            return False
        return True