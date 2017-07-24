from pipig.recipes.models import Recipe
from pipig.recipes.data_setup import recipe_creator

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
        appliance_binders.append((datapoint_id, appliance_id))

    recipe_id = recipe_creator(recipe_name=name, list_of_sensor_binder_tuples=sensor_binders, list_of_appliance_binder_tuples=appliance_binders)
    recipe = Recipe.get(recipe_id)

    return recipe

def create_simple_recipe(data):
    name = data.get('name')
    recipe = Recipe(name=name)
    return recipe