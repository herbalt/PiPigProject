from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for

from pipig.sensors.forms import SensorsForm
from pipig.sensors.models import Sensor
from pipig.data import db

sensors = Blueprint('sensors', __name__)

sensor_index = 'sensors.sensor_list'


@sensors.route('/sensors/add_sensor/', methods=('GET', 'POST'))
def add_sensor():
    form = SensorsForm()
    if form.validate_on_submit():
        name = form.name.data

        sensor_type_id = form.type_id.data
        interval_between_readings = form.interval_between_readings.data

        sensor = Sensor.query.filter_by(name=name).filter_by(type_id=sensor_type_id).filter_by(interval_between_readings=interval_between_readings).first()
        if sensor is not None:
            return redirect(url_for(sensor_index))

        Sensor.create(name=name, type_id=sensor_type_id, interval_between_readings=interval_between_readings)

        return redirect(url_for(sensor_index))
    return render_template('sensors/add.html', form=form)

@sensors.route('/sensors/list/')
def sensor_list():
    return render_template('sensors/sensor_list.html', items=Sensor.query.all())

