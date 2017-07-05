from pipig import app
from pipig.sensors.models import Sensor

def create_sensor(data):
    name = data.get('name')
    type_id = data.get('type_id')
    ibr = data.get('interval_between_readings')
    gpio_pin_id = data.get('gpio_pin_id')

    if gpio_pin_id == 0:
        gpio_pin_id = None

    sensor = Sensor.create(name=name, type_id=type_id, interval_between_readings=ibr, gpio_pin_id=gpio_pin_id)
    return sensor.get_id()
