from test_helpers.test_base import BaseTestCase
from test_helpers.test_generics import unwritten_test


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