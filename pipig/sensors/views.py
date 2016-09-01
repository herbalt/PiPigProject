from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for

from pipig.sensors.forms import SensorsForm
from pipig.sensors.models import Sensor
from pipig.data import db

sensors = Blueprint('sensors', __name__)

sensor_index = 'sensors.sensor_list'


@sensors.route('/sensors/add/', methods=('GET', 'POST'))
def add_sensor():
    form = SensorsForm()
    if form.validate_on_submit():
        name = form.data['name']
        factory_id = form.data['sensor_factory_id']
        interval_between_readings = form.data['interval_between_readings']

        sensor = Sensor.query.filter_by(name=name, sensor_factory_id=factory_id, interval_between_readings=interval_between_readings).first()
        if sensor is not None:
            return redirect(url_for(sensor_index))

        sensor = Sensor(name=name, sensor_factory_id=factory_id, interval_between_readings=interval_between_readings)

        db.session.add(sensor)
        db.session.commit()

        return redirect(url_for(sensor_index))
    return render_template('sensors/add.html', form=form)

@sensors.route('/sensors/list/')
def sensor_list():
    return render_template('sensors/sensor_list.html', items=Sensor.query.all())

