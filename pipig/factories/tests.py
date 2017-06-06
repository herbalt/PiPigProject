from test_helpers.test_base import BaseTestCase
from test_helpers.test_generics import unwritten_test
from factories.abstract_factory import AbstractFactory
from factories.factory import SensorFactory, ApplianceFactory, DatapointFactory
from factories.factory import APPLIANCE_TYPE_NAME_BASIC
from factories.factory import \
    SENSOR_TYPE_NAME_ADC, \
    SENSOR_TYPE_NAME_BASIC, \
    SENSOR_TYPE_NAME_DHT22_CELSIUS, \
    SENSOR_TYPE_NAME_DHT22_FAHRENHEIT, \
    SENSOR_TYPE_NAME_HUMIDITY

from sensors.tests import build_sensor_object
from appliances.tests import build_appliance_object

class AbstractFactoryTests(BaseTestCase):
    def test_build_objects_dict_sensor(self):

        sensor1 = build_sensor_object(base_name="Sensor1", display_units="T", minimum_refresh=1.0, interval_between_readings=1.0)
        sensor2 = build_sensor_object(base_name="Sensor2", display_units="T", minimum_refresh=1.0, interval_between_readings=1.0)
        sensor3 = build_sensor_object(base_name="Sensor3", display_units="T", minimum_refresh=1.0, interval_between_readings=1.0)
        dict_obj = {}
        dict_obj[1] = sensor1
        dict_obj[2] = sensor2
        dict_obj[3] = sensor3

        test_abstract_factory = AbstractFactory()
        sensor_objects = test_abstract_factory.build_objects_dict(test_abstract_factory.SENSOR, [1, 2, 3])

        self.assertDictEqual(sensor_objects, dict_obj, str(sensor_objects) + "\n\n" + str(dict_obj))

    def test_build_objects_dict_appliances(self):
        build_appliance_object(base_name="Appliance1", display_units="A")
        appliance1 = build_appliance_object(base_name="Appliance1", display_units="A")
        appliance2 = build_appliance_object(base_name="Appliance2", display_units="A")
        appliance3 = build_appliance_object(base_name="Appliance3", display_units="A")

        dict_obj = {}
        dict_obj[1] = appliance1
        dict_obj[2] = appliance2
        dict_obj[3] = appliance3

        test_abstract_factory = AbstractFactory()
        appliance_objects = test_abstract_factory.build_objects_dict(test_abstract_factory.APPLIANCE, [1, 2, 3])

        self.assertDictEqual(appliance_objects, dict_obj, str(appliance_objects) + "\n\n" + str(dict_obj))




class FactoryTests(BaseTestCase):
    def test_build_object(self):
        """
        object_id = parameter
        db_obj = self.get_database_object(object_id)
        type_id = db_obj.get_type_id()
        type_obj = self.get_type_object(type_id)
        type_name = type_obj.get_type()
        return self.get_object(type_name, object_id)
        """
        unwritten_test(self)

    def build_object_dict(self):

        """

        :param object_id_list: 
        :return: A Dictionary of Sensor objects where the key is the sensor ID
        
        object_id_list = paramter
        object_dict = {}
        for object_id in object_id_list:
            obj = self.build_object(object_id)
            if not object_dict.has_key(object_id):
                object_dict[object_id] = obj
        return object_dict
        """

        unwritten_test(self)

class FactorySensorTests(BaseTestCase):
    def test_build_object(self):
        unwritten_test(self)

class FactoryApplianceTests(BaseTestCase):
    def test_build_object(self):
        unwritten_test(self)