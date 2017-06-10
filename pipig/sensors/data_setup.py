from pipig import app
from sensors.models import SensorType, Sensor
from generics.models import GenericUnits
# from sensors.factory import SENSOR_TYPE_NAME_BASIC, SENSOR_TYPE_NAME_ADC, SENSOR_TYPE_NAME_DHT22_CELSIUS, SENSOR_TYPE_NAME_DHT22_FAHRENHEIT, SENSOR_TYPE_NAME_HUMIDITY
from factories.factory import SENSOR_TYPE_NAME_BASIC, SENSOR_TYPE_NAME_ADC, SENSOR_TYPE_NAME_DHT22_CELSIUS, SENSOR_TYPE_NAME_DHT22_FAHRENHEIT, SENSOR_TYPE_NAME_HUMIDITY

def data_setup():
    with app.app_context():
        setup_sensor_type()
        setup_testing_sensor()



def setup_sensor_type():
    SensorType.query.delete()
    SensorType.create(type_name=SENSOR_TYPE_NAME_BASIC, units_id=1, minimum_refresh=0.0)
    SensorType.create(type_name=SENSOR_TYPE_NAME_ADC, units_id=2, minimum_refresh=2.0)
    SensorType.create(type_name=SENSOR_TYPE_NAME_DHT22_CELSIUS, units_id=2, minimum_refresh=2.0)
    SensorType.create(type_name=SENSOR_TYPE_NAME_DHT22_FAHRENHEIT, units_id=3, minimum_refresh=2.0)
    SensorType.create(type_name=SENSOR_TYPE_NAME_HUMIDITY, units_id=4, minimum_refresh=2.0)
    return True


def setup_testing_sensor():
    sensor = Sensor.query.filter_by(name='TEST_SENSOR').first()
    if sensor is None:
        Sensor.create(name='TEST_SENSOR', type_id=1, interval_between_readings=0.0)
    return True


if __name__ == '__main__':
    data_setup()