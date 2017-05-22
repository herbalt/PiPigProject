from test_helpers.test_base import BaseTestCase
from pipig.recipes.models import Recipe
from binders.models import BindDatapoitnsAppliances, BindDatapoitnsSensors
from appliances.tests import build_appliance_model
from sensors.tests import build_sensor_model
from data_points.tests import build_datapoints_model


# ________________________________________________________________
#
# Unit Tests
# ________________________________________________________________

class RecipesModelTests(BaseTestCase):
    def test_session_name(self):
        recipe = Recipe.create(name="Name")
        self.assertTrue(recipe.get_name() == "Name")

    def test_get_id(self):
        recipe = build_recipe_model_simple("ID")
        result = recipe.get_id()
        self.assertTrue(result == 1, "ID should equal 1 however is " + str(result))

    def test_sensor_ids(self):
        recipe = build_recipe_model_simple("SENSOR_IDS")
        result = recipe.get_sensor_ids()
        self.assertListEqual(result, [1, 2], "Sensor IDs from recipe are incorrect " + str(result))

    def test_appliance_ids(self):
        recipe = build_recipe_model_simple("APPLIANCE_IDS")
        result = recipe.get_appliance_ids()
        self.assertListEqual(result, [1, 2], "Appliance IDs from recipe are incorrect " + str(result))

    def test_datapoints_ids(self):
        recipe = build_recipe_model_simple("DATAPOINTS_IDS")
        result = recipe.get_datapoints_ids()
        self.assertListEqual(result, [1, 2], "Datapoints IDs from recipe are incorrect " + str(result))

    def test_sensor_datapoints_binding_ids(self):
        recipe = build_recipe_model_simple("SENSOR_BINDERS_IDS")
        result = recipe.get_sensor_datapoints_binding_ids()
        self.assertListEqual(result, [1, 2], "Sensor Datapoints IDs from recipe are incorrect " + str(result))

    def test_appliance_datapoints_binding_ids(self):
        recipe = build_recipe_model_simple("APPLIANCE_BINDERS_IDS")
        result = recipe.get_appliance_datapoints_binding_ids()
        self.assertListEqual(result, [1, 2], "Appliance Datapoints IDs from recipe are incorrect " + str(result))


# ________________________________________________________________
#
# Builders to use in Unit Tests
# ________________________________________________________________
def build_recipe_model_simple(base_name):
    recipe = Recipe.create(name="%sRecipeModel" % base_name)
    recipe_id = recipe.get_id()

    appliance_ids = yeild_object_ids(build_appliances(3))
    sensor_ids = yeild_object_ids(build_sensors(3))
    dps = build_datapoints(3)
    datapoints_ids = yeild_object_ids(dps)

    binders_sensor_ids = yeild_object_ids(build_sensor_binders(recipe_id, ((1, 1), (2, 2))))
    binders_appliance_ids = yeild_object_ids(build_appliance_binders(recipe_id, ((1, 1), (2, 2))))

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
            BindDatapoitnsSensors.create(recipe_id=recipe_id, datapoints_id=tuple_binder[1], sensor_id=tuple_binder[0]))
    return binders


def build_appliance_binders(recipe_id, tuple_list_of_appliance_datapoints):
    binders = []
    for tuple_binder in tuple_list_of_appliance_datapoints:
        binders.append(
            BindDatapoitnsAppliances.create(recipe_id=recipe_id, datapoints_id=tuple_binder[1], appliance_id=tuple_binder[0]))
    return binders
