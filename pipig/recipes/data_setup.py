from binders.models import BindDatapointsSensors, BindDatapointsAppliances
from recipes.models import Recipe
from pipig import app


def define_bind_datapoints_sensors(recipe_id, list_of_sensor_binder_tuples):
    """
    list_of_sensor_binder_tuples: (datapoints_id, sensor_id)
    Example: [(1,2), (2,2), (1,1))

    A list of the IDs for the relevant Sensors Binders to use in the trial
    :return: list_of_sensor_binder_ids
    """
    list_of_sensor_binder = []
    for binder_tuple in list_of_sensor_binder_tuples:
        with app.app_context():
            binder = BindDatapointsSensors.create(recipe_id=recipe_id, datapoints_id=binder_tuple[0], sensor_id=binder_tuple[1])
            list_of_sensor_binder.append(binder.id)
    return list_of_sensor_binder


def define_bind_datapoints_appliances(recipe_id, list_of_appliance_binder_tuples):
    """
    list_of_appliance_binder_tuples: (datapoints_id, appliance_id, polarity)
    Example: [(1, 2, -1), (2, 4, 1), (1, 5, 1))

    A list of the IDs for the relevant Appliance Binders to use in the trial
    :return: list_of_sensor_binder_ids
    """
    list_of_appliance_binder = []
    for binder_tuple in list_of_appliance_binder_tuples:
        with app.app_context():
            binder = BindDatapointsAppliances.create(recipe_id=recipe_id, datapoints_id=binder_tuple[0],
                                                  appliance_id=binder_tuple[1])
            list_of_appliance_binder.append(binder.id)
    return list_of_appliance_binder


def recipe_creator(recipe_name="", list_of_sensor_binder_tuples=[],
                            list_of_appliance_binder_tuples=[]):
    with app.app_context():
        recipe = Recipe.create(name=recipe_name)
    # Binder Tuple Storage
        recipe_id = recipe.get_id()
    define_bind_datapoints_sensors(recipe_id, list_of_sensor_binder_tuples)
    define_bind_datapoints_appliances(recipe_id, list_of_appliance_binder_tuples)
    return recipe_id