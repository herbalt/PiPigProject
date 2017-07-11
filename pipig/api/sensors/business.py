from sqlalchemy.orm.exc import NoResultFound

from pipig.sensors.models import Sensor, SensorType
from pipig.generics.models import GenericUnits
from pipig.pi_gpio.models import GpioPin



def get_sensor(sensor_model):

    type_id = sensor_model.get_type_id()
    sensor_type = SensorType.query.filter(SensorType.id == type_id).one()
    units_id = sensor_type.get_units_id()
    units = GenericUnits.query.filter(GenericUnits.id == units_id).one()
    try:
        gpio_pin = GpioPin.query.filter(GpioPin.id == sensor_model.get_gpio_pin_id()).one()
    except NoResultFound:
        gpio_pin = GpioPin(None, None, None, 'No GPIO Connection')

    sensor_dict = {
        'sensor': {
            'id': sensor_model.get_id(),
            'name': sensor_model.get_name(),
            'sensor type': {
                'type id': sensor_type.get_id(),
                'type name': sensor_type.get_type(),
                'unit name': units.get_code_name(),
                'unit display name': units.get_display_units()
            },
            'gpio': {
                'pin number': gpio_pin.get_pin_number(),
                'pin name': gpio_pin.get_pin_name()
            }
        }
    }

    return sensor_dict


def create_sensor(data):
    name = data.get('name')
    type_id = data.get('type_id')
    ibr = data.get('interval_between_readings')
    gpio_pin_id = data.get('gpio_pin_id')

    sensor_type = SensorType.get(type_id)
    units = sensor_type.get_units_id()
    if sensor_type is None or units is None:
        return None

    if gpio_pin_id == 0:
        gpio_pin_id = None
    else:
        gpio = GpioPin.get(gpio_pin_id)
        if gpio is None:
            return None

    sensor = Sensor.create(name=name, type_id=type_id, interval_between_readings=ibr, gpio_pin_id=gpio_pin_id)
    return sensor


def update_sensor(sensor_id, data):
    type_id = data.get('type_id')
    name = data.get('name')
    gpio_pin_id = data.get('gpio_pin_id')
    ibr = data.get('interval_between_readings')

    sensor = Sensor.query.filter_by(id=sensor_id).one()

    sensor_type = SensorType.get(type_id)
    if sensor_type is None:
        raise NoResultFound

    unit_model = GenericUnits.get(sensor_type.get_units_id())
    if unit_model is None:
        raise NoResultFound

    if type_id is not None:
        sensor.update(type_id=type_id)

    if name is not None:
        sensor.update(name=name)

    if ibr is not None:
        sensor.update(interval_between_readings=ibr)

    if gpio_pin_id is not 0:
        sensor.update(gpio_pin_id=gpio_pin_id)

    return sensor