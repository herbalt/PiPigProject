from sensors.models import Sensor, SensorType
from sensors.sensor import SensorBasic, SensorADC, SensorDHT22Temperature, SensorDHT22Humidity



SENSOR_TYPE_NAME_BASIC = 'Counter'
SENSOR_TYPE_NAME_ADC = 'ADC Temparture'
SENSOR_TYPE_NAME_DHT22_CELSIUS = 'DHT22 Celsius'
SENSOR_TYPE_NAME_DHT22_FAHRENHEIT = 'DHT22 Fahrenheit'
SENSOR_TYPE_NAME_HUMIDITY = 'DHT22 Humidity'

class FactorySensor:

    def build_object(self, sensor_id):

        # db_obj = Sensor.query.filter_by(id=sensor_id).first()
        db_obj = Sensor.get(sensor_id)
        sensor_type_id = db_obj.get_type_id()
        sensor_type = SensorType.get(sensor_type_id)

        type_name = sensor_type.get_type()
        if type_name == SENSOR_TYPE_NAME_BASIC:
            return SensorBasic(sensor_id)

        elif type_name == SENSOR_TYPE_NAME_ADC:
            return SensorADC(sensor_id)

        elif type_name == SENSOR_TYPE_NAME_DHT22_CELSIUS:
            return SensorDHT22Temperature(sensor_id, True)

        elif type_name == SENSOR_TYPE_NAME_DHT22_FAHRENHEIT:
            return SensorDHT22Temperature(sensor_id, False)

        elif type_name == SENSOR_TYPE_NAME_HUMIDITY:
            return SensorDHT22Humidity(sensor_id)

        else:
            return None



