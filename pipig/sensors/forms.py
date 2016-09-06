from flask_wtf import Form
from wtforms import fields
import wtforms.validators as validators

import pipig.sensors.models as sensors


class SensorsForm(Form):

    name = fields.StringField(validators=[validators.InputRequired()])
    sensor_type_id = fields.IntegerField(validators=[validators.InputRequired()])
    interval_between_readings = fields.FloatField()


    @staticmethod
    def populate(name='', sensor_type_id=-1, interval_between_readings=-1):
        obj = SensorsForm()

        obj.name.data = name
        obj.sensor_type_id.data = sensor_type_id
        obj.interval_between_readings.data = interval_between_readings
        return obj

    def validate_name(form, field):
        # name = sensors.Sensor.query.filter_by(name=form.name).first()
        if form.name.data == '':
            return False
        return True

    def validate_sensor_type_id(form, field):
        if form.sensor_type_id < 0:
            return False
        sensor_type_id = sensors.SensorType.query.filter_by(id=form.sensor_type_id.data).first()
        if sensor_type_id is None:
            return False

        return True

    def validate_interval_between_readings(form, field):

        minimum_search = sensors.SensorType.query.filter_by(id=form.sensor_type_id.data).first()
        if minimum_search is not None:
            if minimum_search.minimum_refresh > form.interval_between_readings.data:
                return False

        if form.interval_between_readings.data < 0:
            return False
        return True