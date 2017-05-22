from test_helpers.test_base import BaseTestCase
from binders.models import BindDatapoitnsSensors, BindDatapoitnsAppliances


class BindDataPointsSensorModelTests(BaseTestCase):
    def build_test_obj(self):
        return build_sensor_binder()

    def test_get_id(self):
        obj = self.build_test_obj()
        self.assertTrue(type(obj) == BindDatapoitnsSensors)
        self.assertTrue(obj.get_id() == 1, "%s\n should produce an ID of 1" % str(obj))

    def test_get_datapoint_id(self):
        obj = self.build_test_obj()
        self.assertTrue(type(obj) == BindDatapoitnsSensors)
        self.assertTrue(obj.get_datapoints_id() == 1, "%s\n should produce an DataPoint ID of 1" % str(obj))

    def get_recipe_id(self):
        obj = self.build_test_obj()
        self.assertTrue(type(obj) == BindDatapoitnsSensors)
        self.assertTrue(obj.get_recipe_id() == 1, "%s\n should produce an Recipe ID of 1" % str(obj))

    def test_get_sensor_id(self):
        obj = self.build_test_obj()
        self.assertTrue(type(obj) == BindDatapoitnsSensors)
        self.assertTrue(obj.get_sensor_id() == 1, "%s\n should produce an SessionSensor ID of 1" % str(obj))


class BindDataPointsApplianceModelTests(BaseTestCase):
    def build_test_obj(self):
        return build_appliance_binder()

    def test_get_id(self):
        obj = self.build_test_obj()
        self.assertTrue(type(obj) == BindDatapoitnsAppliances)
        self.assertTrue(obj.get_id() == 1, "%s\n should produce an ID of 1" % str(obj))

    def test_get_datapoint_id(self):
        obj = self.build_test_obj()
        self.assertTrue(type(obj) == BindDatapoitnsAppliances)
        self.assertTrue(obj.get_datapoints_id() == 1, "%s\n should produce an DataPoint ID of 1" % str(obj))

    def get_recipe_id(self):
        obj = self.build_test_obj()
        self.assertTrue(type(obj) == BindDatapoitnsAppliances)
        self.assertTrue(obj.get_recipe_id() == 1, "%s\n should produce an Recipe ID of 1" % str(obj))

    def test_get_appliance_id(self):
        obj = self.build_test_obj()
        self.assertTrue(type(obj) == BindDatapoitnsAppliances)
        self.assertTrue(obj.get_appliance_id() == 1, "%s\n should produce an Appliance ID of 1" % str(obj))



def build_sensor_binder(recipe_id=1, datapoints_id=1, sensor_id=1):
    sensor_binder = BindDatapoitnsSensors.create(recipe_id=recipe_id, datapoints_id=datapoints_id, sensor_id=sensor_id)
    return sensor_binder

def build_appliance_binder(recipe_id=1, datapoints_id=1, appliance_id=1):
    appliance_binder = BindDatapoitnsAppliances.create(recipe_id=recipe_id, datapoints_id=datapoints_id, appliance_id=appliance_id)
    return appliance_binder