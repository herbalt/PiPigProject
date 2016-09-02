from sensors.models import SensorType, SensorUnits


def run_setup():
    setup_sensor_type()
    setup_sensor_units()


def setup_sensor_type():
    SensorType.query.delete()
    SensorType.create(sensor_type='Counter', sensor_units_id=1, minimum_refresh=0.0)
    SensorType.create(sensor_type='ADC Temparture', sensor_units_id=2, minimum_refresh=2.0)
    SensorType.create(sensor_type='DHT22 Celsius', sensor_units_id=2, minimum_refresh=2.0)
    SensorType.create(sensor_type='DHT22 Fahrenheit', sensor_units_id=3, minimum_refresh=2.0)
    SensorType.create(sensor_type='DHT22 Humidity', sensor_units_id=4, minimum_refresh=2.0)
    return True


def setup_sensor_units():
    SensorUnits.query.delete()
    SensorUnits.create(code_name='COUNTER', display_units='')
    SensorUnits.create(code_name='CELCIUS', display_units='C')
    SensorUnits.create(code_name='FAHRENHEIT', display_units='F')
    SensorUnits.create(code_name='HUMIDITY', display_units='H')
    return True

