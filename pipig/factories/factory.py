from abc import abstractmethod, ABCMeta

from sensors.models import Sensor, SensorType
from sensors.sensor import SensorBasic, SensorADC, SensorDHT22Temperature, SensorDHT22Humidity
from appliances.appliance import BasicAppliance, RelayAppliance
from appliances.models import Appliance, ApplianceType
from data_points.models import DataPoints
from binders.models import BindDatapointsAppliances
from pipig import app

SENSOR_TYPE_NAME_BASIC = 'Counter'
SENSOR_TYPE_NAME_ADC = 'ADC Temparture'
SENSOR_TYPE_NAME_DHT22_CELSIUS = 'DHT22 Celsius'
SENSOR_TYPE_NAME_DHT22_FAHRENHEIT = 'DHT22 Fahrenheit'
SENSOR_TYPE_NAME_HUMIDITY = 'DHT22 Humidity'

APPLIANCE_TYPE_NAME_BASIC = 'Basic Appliance'
APPLIANCE_TYPE_NAME_RELAY = 'Relay Appliance'


class BaseFactory:
    __metaclass__ = ABCMeta

    def build_object(self, object_id):
        db_obj = self.get_database_object(object_id)

        try:
            type_id = db_obj.get_type_id()
            type_obj = self.get_type_object(type_id)
            type_name = type_obj.get_type()
        except:
            type_name = "NoType"

        return self.get_object(type_name, object_id)

    def build_object_dict(self, object_id_list):

        """

        :param object_id_list: 
        :return: A Dictionary of Sensor objects where the key is the serial_sensor ID
        """
        object_dict = {}
        for object_id in object_id_list:
            obj = self.build_object(object_id)
            if not object_dict.has_key(object_id):
                object_dict[object_id] = obj
        return object_dict

    @abstractmethod
    def get_database_object(self, object_id):
        return None

    @abstractmethod
    def get_type_object(self, type_id):
        return None

    @abstractmethod
    def get_object(self, lookup_value, object_id):
        """
        
        :param object_id: The id value of the object to initiate
        :param lookup_value: The input value for the Switch Statement that outputs the specific value
        :return: The fully initiated object
        """
        return None


class ApplianceFactory(BaseFactory):
    def get_database_object(self, object_id):
        with app.app_context():
            appliance = Appliance.get(id=object_id)
        return appliance

    def get_type_object(self, type_id):
        with app.app_context():
            appliance_type = ApplianceType.get(type_id)
        return appliance_type

    def get_object(self, lookup_value, object_id):
        if lookup_value == APPLIANCE_TYPE_NAME_BASIC:
            return BasicAppliance(object_id)
        if lookup_value == APPLIANCE_TYPE_NAME_RELAY:
            return RelayAppliance(object_id)
        else:
            return BasicAppliance(object_id)


class SensorFactory(BaseFactory):
    def get_object(self, lookup_value, object_id):
        if lookup_value == SENSOR_TYPE_NAME_BASIC:
            return SensorBasic(object_id)

        elif lookup_value == SENSOR_TYPE_NAME_ADC:
            return SensorADC(object_id)

        elif lookup_value == SENSOR_TYPE_NAME_DHT22_CELSIUS:
            return SensorDHT22Temperature(object_id, True)

        elif lookup_value == SENSOR_TYPE_NAME_DHT22_FAHRENHEIT:
            return SensorDHT22Temperature(object_id, False)

        elif lookup_value == SENSOR_TYPE_NAME_HUMIDITY:
            return SensorDHT22Humidity(object_id)

        else:
            return SensorBasic(object_id)

    def get_database_object(self, object_id):
        # with app.app_context():
        sensor = Sensor.get(id=object_id)
        return sensor

    def get_type_object(self, type_id):
        # with app.app_context():
        sensor_type = SensorType.get(id=type_id)
        return sensor_type


class DatapointFactory(BaseFactory):
    def get_object(self, lookup_value, object_id):
        # with app.app_context():
        datapoints = DataPoints.get(object_id)
        return datapoints

    def get_type_object(self, type_id):
        return "DATAPOINTS"

    def get_database_object(self, object_id):
        return DataPoints.get(object_id)


class ApplianceBinderFactory:

    def __init__(self):
        pass

    def build_object(self, object_id):
        db_obj = self.get_database_object(object_id)
        return db_obj

    def build_object_dict(self, object_id_list):
        object_dict = {}
        for object_id in object_id_list:
            obj = self.build_object(object_id)
            if not object_dict.has_key(object_id):
                object_dict[object_id] = obj
        return object_dict

    def get_database_object(self, object_id):
        with app.app_context():
            binder = BindDatapointsAppliances.get(object_id)
        return binder
