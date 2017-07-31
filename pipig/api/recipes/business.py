from recipes.models import Recipe
from recipes.data_setup import recipe_creator

from binders.models import BindDatapointsSensors, BindDatapointsAppliances
from data_points.models import DataPoints
from sensors.models import Sensor
from appliances.models import Appliance

def get_recipe_detail(recipe):
    """
    Takes a Recipe Python Model and converts all the IDs into objects and creates the detailed Recipe JSON
    :param recipe: The Recipe Python Model
    :return: The Detailed JSON Recipe Object
    """
    sensor_binder_ids = recipe.get_sensor_datapoints_binding_ids()
    appliance_binder_ids = recipe.get_appliance_datapoints_binding_ids()

    sensor_binder_list = []

    for sensor_binder_id in sensor_binder_ids:
        binder = BindDatapointsSensors.get(sensor_binder_id)
        datapoint_id = binder.get_datapoints_id()
        sensor_id = binder.get_sensor_id()
        datapoints = DataPoints.get(datapoint_id)
        sensor = Sensor.get(sensor_id)
        datapoints_json = datapoints.get_json()
        sensor_json = sensor.get_json()
        binder_json = {'datapoint': datapoints_json, 'sensor': sensor_json}
        sensor_binder_list.append(binder_json)

    appliance_binder_list = []

    for appliance_binder_id in appliance_binder_ids:
        binder = BindDatapointsAppliances.get(appliance_binder_id)
        datapoint_id = binder.get_datapoints_id()
        appliance_id = binder.get_appliance_id()
        datapoints = DataPoints.get(datapoint_id)
        appliance = Appliance.get(appliance_id)
        datapoints_json = datapoints.get_json()
        appliance_json = appliance.get_json()
        binder_json = {'datapoint': datapoints_json, 'appliance': appliance_json, 'polarity': binder.get_polarity()}
        appliance_binder_list.append(binder_json)

    json_response = {
        'recipe base': {
            'recipe id': recipe.get_id(),
            'name': recipe.get_name()
        },
        'list of sensor bindings': sensor_binder_list,
        'list of appliance bindings': appliance_binder_list
    }

    return json_response

def create_recipe_from_tuples(data):
    """
    Creates a new Recipe from a JSON Object that contains all the tuples
    :param data:
    :return:
    """
    name = data.get('name')
    list_of_sensor_bindings = data.get('list of sensor binders')
    list_of_appliance_bindings = data.get('list of appliance binders')
    list_of_appliance_bindings = list_of_appliance_bindings.encode('ascii', 'ignore')

    recipe_id = recipe_creator(recipe_name=name, list_of_sensor_binder_tuples=list_of_sensor_bindings,
                               list_of_appliance_binder_tuples=list_of_appliance_bindings)
    recipe = Recipe.get(recipe_id)

    return recipe


def create_recipe(data):
    """
    Creates a new Recipe from JSON Data
    :param data: The JSON Object (mainly IDs of the relevant components)
    :return: The Recipe Model Object
    """
    name = data.get('name')
    list_of_sensor_bindings = data.get('list of sensor bindings')
    list_of_appliance_bindings = data.get('list of appliance bindings')

    sensor_binders = []
    for binder in list_of_sensor_bindings:
        sensor_id = binder.get('sensor id')
        datapoint_id = binder.get('datapoint id')
        sensor_binders.append((datapoint_id, sensor_id))

    appliance_binders = []
    for binder in list_of_appliance_bindings:
        appliance_id = binder.get('appliance id')
        datapoint_id = binder.get('datapoint id')
        polarity = binder.get('polarity')
        appliance_binders.append((datapoint_id, appliance_id, polarity))

    recipe_id = recipe_creator(recipe_name=name, list_of_sensor_binder_tuples=sensor_binders, list_of_appliance_binder_tuples=appliance_binders)
    recipe = Recipe.get(recipe_id)

    return recipe

def create_simple_recipe(data):
    name = data.get('name')
    recipe = Recipe(name=name)
    return recipe