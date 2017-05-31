from test_helpers.test_base import BaseTestCase
from test_helpers.test_generics import run_equals_test, unwritten_test
from binders.models import BindDatapointsSensors, BindDatapointsAppliances


#________________________________________________________________
#
# Unit Tests
#________________________________________________________________
class BindDataPointsSensorModelTests(BaseTestCase):

    def test_get_id(self):
        obj = build_sensor_binder()
        run_equals_test(self, type(obj), BindDatapointsSensors, "BindSensorDataPointsID", "Object type is correct")
        run_equals_test(self, obj.get_id(), 1, "BindSensorDataPointsID", "Get ID Method")

    def test_get_datapoint_id(self):
        obj = build_sensor_binder()
        run_equals_test(self, type(obj), BindDatapointsSensors, "BindSensorDataPointsID", "Object type is correct")
        run_equals_test(self, obj.get_datapoints_id(), 1, "BindSensorDataPointsID", "Get Datapoints ID Method")

    def get_recipe_id(self):
        obj = build_sensor_binder()
        run_equals_test(self, type(obj), BindDatapointsSensors, "BindSensorDataPointsID", "Object type is correct")
        run_equals_test(self, obj.get_recipe_id(), 1, "BindSensorDataPointsID", "Get Recipe ID Method")

    def test_get_sensor_id(self):
        obj = build_sensor_binder()
        run_equals_test(self, type(obj), BindDatapointsSensors, "BindSensorDataPointsID", "Object type is correct")
        run_equals_test(self, obj.get_sensor_id(), 1, "BindSensorDataPointsID", "Get Sensor ID Method")


class BindDataPointsApplianceModelTests(BaseTestCase):

    def test_get_id(self):
        obj = build_appliance_binder()
        run_equals_test(self, type(obj), BindDatapointsAppliances, "BindApplianceDataPointsID", "Object type is correct")
        run_equals_test(self, obj.get_id(), 1, "BindApplianceDataPointsID", "Get ID Method")

    def test_get_datapoint_id(self):
        obj = build_appliance_binder()
        run_equals_test(self, type(obj), BindDatapointsAppliances, "BindApplianceDataPointsID",
                        "Object type is correct")
        run_equals_test(self, obj.get_datapoints_id(), 1, "BindApplianceDataPointsID", "Get DataPoints ID Method")

    def get_recipe_id(self):
        obj = build_appliance_binder()
        run_equals_test(self, type(obj), BindDatapointsAppliances, "BindApplianceDataPointsID",
                        "Object type is correct")
        run_equals_test(self, obj.get_recipe_id(), 1, "BindApplianceDataPointsID", "Get Recipe ID Method")

    def test_get_appliance_id(self):
        obj = build_appliance_binder()
        run_equals_test(self, type(obj), BindDatapointsAppliances, "BindApplianceDataPointsID",
                        "Object type is correct")
        run_equals_test(self, obj.get_appliance_id(), 1, "BindApplianceDataPointsID", "Get Appliance ID Method")

    def test_get_polarity(self):
        obj = build_appliance_binder()

        obj.polarity = 5
        run_equals_test(self, obj.get_polarity(), 1, "BindApplianceDataPointsID", "Get Appliance ID Method")
        obj.polarity = 1
        run_equals_test(self, obj.get_polarity(), 1, "BindApplianceDataPointsID", "Get Appliance ID Method")
        obj.polarity = 0
        run_equals_test(self, obj.get_polarity(), 0, "BindApplianceDataPointsID", "Get Appliance ID Method")
        obj.polarity = -5
        run_equals_test(self, obj.get_polarity(), -1, "BindApplianceDataPointsID", "Get Appliance ID Method")
        obj.polarity = -1
        run_equals_test(self, obj.get_polarity(), -1, "BindApplianceDataPointsID", "Get Appliance ID Method")
        obj.polarity = None
        run_equals_test(self, obj.get_polarity(), 1, "BindApplianceDataPointsID", "Get Appliance ID Method")

    def test_response_to_datapoint(self):
        unwritten_test(self)
#________________________________________________________________
#
# Builders for Tests
#________________________________________________________________
def build_sensor_binder(recipe_id=1, datapoints_id=1, sensor_id=1):
    sensor_binder = BindDatapointsSensors.create(recipe_id=recipe_id, datapoints_id=datapoints_id, sensor_id=sensor_id)
    return sensor_binder


def build_appliance_binder(recipe_id=1, datapoints_id=1, appliance_id=1):
    appliance_binder = BindDatapointsAppliances.create(recipe_id=recipe_id, datapoints_id=datapoints_id, appliance_id=appliance_id)
    return appliance_binder