from pipig import app
from sensors.models import SensorType, Sensor
from generics.models import GenericUnits
from factories.factory import SENSOR_TYPE_NAME_BASIC, SENSOR_TYPE_NAME_ADC, SENSOR_TYPE_NAME_DHT22_CELSIUS, SENSOR_TYPE_NAME_DHT22_FAHRENHEIT, SENSOR_TYPE_NAME_HUMIDITY


def data_setup():
    with app.app_context():
        print str(setup_sensor_type())
        print str(setup_testing_sensor())



def setup_sensor_type():
    sensor_list_ids = []
    sensor_list_ids.append(helper_setup_sensor_type(SENSOR_TYPE_NAME_BASIC, units_id=1, minimum_refresh=0.0))
    sensor_list_ids.append(helper_setup_sensor_type(SENSOR_TYPE_NAME_ADC, units_id=2, minimum_refresh=2.0))
    sensor_list_ids.append(helper_setup_sensor_type(SENSOR_TYPE_NAME_DHT22_CELSIUS, units_id=2, minimum_refresh=2.0))
    sensor_list_ids.append(helper_setup_sensor_type(SENSOR_TYPE_NAME_DHT22_FAHRENHEIT, units_id=3, minimum_refresh=2.0))
    sensor_list_ids.append(helper_setup_sensor_type(SENSOR_TYPE_NAME_HUMIDITY, units_id=4, minimum_refresh=2.0))
    return sensor_list_ids


def setup_testing_sensor():
    sensor_list_ids = []
    sensor_list_ids.append(helper_setup_sensors(factory_type_constant=SENSOR_TYPE_NAME_BASIC, sensor_name="TEST_SENSOR", interval_between_readings=0.0, gpio_pin_id=None))
    return sensor_list_ids


def helper_setup_sensor_type(factory_constant, units_id, minimum_refresh=2.0):
    sensor_type = SensorType.query.filter_by(type_name=factory_constant).first()
    sensor_type_id = None
    if sensor_type is None:
        sensor_type_obj = SensorType.create(type_name=factory_constant, units_id=units_id, minimum_refresh=minimum_refresh)
        sensor_type_id = sensor_type_obj.get_id()
    return sensor_type_id


def helper_setup_sensors(factory_type_constant, sensor_name, interval_between_readings=1.0, gpio_pin_id=None):
    sensor = Sensor.query.filter_by(name=sensor_name).first()
    sensor_id = None
    if sensor is None:
        # TODO This might need to be more selective of what type object it is trying to find

        sensor_type = SensorType.query.filter_by(type_name=factory_type_constant).first()
        sensor_obj = Sensor.create(name=sensor_name, type_id=sensor_type.get_id(), interval_between_readings=interval_between_readings, gpio_pin_id=gpio_pin_id)
        sensor_id = sensor_obj.get_id()
    return sensor_id


if __name__ == '__main__':
    data_setup()