from test_helpers.test_base import BaseTestCase
from test_helpers.test_generics import run_equals_test, run_list_equals_test, unwritten_test
from pipig.recipes.models import Recipe
from binders.models import BindDatapointsAppliances, BindDatapointsSensors
from appliances.tests import build_appliance_model
from sensors.tests import build_sensor_model
from data_points.tests import build_datapoints_model


# ________________________________________________________________
#
# Unit Tests
# ________________________________________________________________

class RecipesModelTests(BaseTestCase):
    def test_session_name(self):
        recipe = Recipe.create(name="Salami")
        run_equals_test(self, recipe.get_name(), "Salami", "Session Name", "Should be able to set and retrieve a name of the Recipe")

    def test_get_id(self):
        recipe = build_recipe_model("ID")
        result = recipe.get_id()
        run_equals_test(self, result, 1, "Get ID", "Get ID from Recipe Failed")

    def test_sensor_ids(self):
        recipe = build_recipe_model("SENSOR_IDS")
        result = recipe.get_sensor_ids()
        run_list_equals_test(self, result, [1, 2], "Sensor IDs", "getSensorIds failed")

    def test_appliance_ids(self):
        recipe = build_recipe_model("APPLIANCE_IDS")
        result = recipe.get_appliance_ids()
        run_list_equals_test(self, result, [1, 2], "Appliance IDs", "getApplianceIds failed")

    def test_datapoints_ids(self):
        recipe = build_recipe_model("DATAPOINTS_IDS")
        result = recipe.get_datapoints_ids()
        run_list_equals_test(self, result, [1, 2], "Datapoints IDs", "getDatapointsIds failed")

    def test_sensor_datapoints_binding_ids(self):
        recipe = build_recipe_model("SENSOR_BINDERS_IDS")
        result = recipe.get_sensor_datapoints_binding_ids()
        run_list_equals_test(self, result, [1, 2, 3], "Sensor Datapoints Binder IDs", "get_sensor_datapoints_binding_ids failed")

    def test_appliance_datapoints_binding_ids(self):
        recipe = build_recipe_model("APPLIANCE_BINDERS_IDS")
        result = recipe.get_appliance_datapoints_binding_ids()
        run_list_equals_test(self, result, [1, 2, 3, 4], "Appliance Datapoints Binder IDs",
                             "get_appliance_datapoints_binding_ids failed")

    def test_get_datapoints_for_sensor(self):
        unwritten_test(self)

    def test_get_appliances_for_datapoint(self):
        unwritten_test(self)

# ________________________________________________________________
#
# Builders to use in Unit Tests
# ________________________________________________________________
def build_recipe_model(base_name, sensor_count=3, appliance_count=3, datapoints_count=3, sensor_binder_tuples=((1, 1), (2, 2), (1, 2)), appliance_binder_tuples=((1, 1), (2, 2), (1, 2), (2, 1))):
    recipe = Recipe.create(name="%sRecipeModel" % base_name)
    recipe_id = recipe.get_id()

    appliance_ids = yeild_object_ids(build_appliances(appliance_count))
    sensor_ids = yeild_object_ids(build_sensors(sensor_count))
    datapoints_ids = yeild_object_ids(build_datapoints(datapoints_count))

    binders_sensor_ids = yeild_object_ids(build_sensor_binders(recipe_id, sensor_binder_tuples))
    binders_appliance_ids = yeild_object_ids(build_appliance_binders(recipe_id, appliance_binder_tuples))

    return recipe


def yeild_object_ids(object_list):
    id_list = []
    for obj in object_list:
        id_list.append(obj.get_id())
    return id_list


def build_appliances(number_of_objects=1):
    "Builds a list of Mock appliances for testing"
    appliance_list = []
    for i in range(number_of_objects):
        appliance_list.append(build_appliance_model(base_name="app_test_" + str(i), display_units="APP"))
    return appliance_list


def build_sensors(number_of_objects=1):
    "Builds a list of Mock sensors for testing"
    sensor_list = []
    for i in range(number_of_objects):
        sensor_list.append(build_sensor_model(base_name="sensor_test_" + str(i), display_units="APP", minimum_refresh=0,
                                              interval_between_readings=2))
    return sensor_list


def build_datapoints(number_of_objects=1):
    datapoints_list = []
    for i in range(number_of_objects):
        datapoints_list.append(build_datapoints_model(base_name="datapoints_test_" + str(i), list_of_points_as_tuples=((1, 0), (2, 1))))
    return datapoints_list


def build_sensor_binders(recipe_id, tuple_list_of_sensor_datapoints):
    binders = []
    for tuple_binder in tuple_list_of_sensor_datapoints:
        binders.append(
            BindDatapointsSensors.create(recipe_id=recipe_id, datapoints_id=tuple_binder[1], sensor_id=tuple_binder[0]))
    return binders


def build_appliance_binders(recipe_id, tuple_list_of_appliance_datapoints):
    binders = []
    for tuple_binder in tuple_list_of_appliance_datapoints:
        binders.append(
            BindDatapointsAppliances.create(recipe_id=recipe_id, datapoints_id=tuple_binder[1], appliance_id=tuple_binder[0]))
    return binders

# ________________________________________________________________
#
# Mock Object for Unit Tests
# ________________________________________________________________
class MockRecipe(Recipe):
    def __init__(self, name, self_id=1, appliance_ids=[1, 2],
                 sensor_ids=[1, 2], datapoints_ids=[1, 2], sensor_binder_ids=[1, 2, 3], appliance_binder_ids=[1, 2, 3, 4]):
        super(MockRecipe, self).__init__(name)
        self.self_id = self_id
        self.appliance_ids = appliance_ids
        self.sensor_ids = sensor_ids
        self.datapoints_ids = datapoints_ids
        self.sensor_binder_ids = sensor_binder_ids
        self.appliance_binder_ids = appliance_binder_ids

    def get_id(self):
        return self.self_id

    def get_name(self):
        return self.name

    def get_appliance_ids(self):
        return self.appliance_ids

    def get_sensor_ids(self):
        return self.sensor_ids

    def get_datapoints_ids(self):
        return self.datapoints_ids

    def get_sensor_datapoints_binding_ids(self):
        return self.sensor_binder_ids

    def get_appliance_datapoints_binding_ids(self):
        return self.appliance_binder_ids

