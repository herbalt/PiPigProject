from flask import request
from flask_restplus import Resource

from api.sensors.business import create_sensor, update_sensor
from api.sensors.serializers import serial_sensor , serial_new_sensor
from pipig.api import api as api_plus
from pipig.recipes.models import Recipe
from pipig.sensors.models import Sensor

recipe_namespace = api_plus.namespace('recipes',
                                      description='Instructions for a monitored and controlled Charcuterie Chamber operation')


@recipe_namespace.route('<int:recipe_id>/sensors')
class RecipeSensorItems(Resource):
    @recipe_namespace.marshal_list_with(serial_sensor)
    @recipe_namespace.response(code=200, description='The list of JSON sensors that relate to a Recipe', model=serial_sensor)
    def get(self, recipe_id):
        """
        Get all the Sensors that are associated with a particular recipe
        :param recipe_id:
        :return: List of Sensor JSON Objects
        """
        recipe = Recipe.get(recipe_id)
        sensor_ids = recipe.get_sensor_ids()
        list_of_sensors = []

        for sensor_id in sensor_ids:
            sensor = Sensor.get(sensor_id)
            list_of_sensors.append(sensor)

        return list_of_sensors
