from flask import request
from flask_restplus import abort
from flask_restplus import Resource

from pipig.api.recipes.business import create_recipe, create_simple_recipe
from pipig.api.recipes.serializers import serial_recipe
from api.sensors.serializers import serial_sensor
from pipig.api import api as api_plus
from pipig.recipes.models import Recipe
from pipig.sensors.models import Sensor

recipe_namespace = api_plus.namespace('recipes',
                                      description='Instructions for a monitored and controlled Charcuterie Chamber operation')


@recipe_namespace.route('/')
class Recipe(Resource):

    @recipe_namespace.marshal_list_with(serial_recipe)
    @recipe_namespace.response(200, description='Returned a list of all Recipes')
    @recipe_namespace.response(500, description='Failed to retrieve Recipe list, check if all component IDs exist')
    def get(self):
        """
        Returns list of all Recipes stored in the Database.
        The JSON Object will contain all the Nested Fields for the Binders in the Recipe.
        """

        recipes = Recipe.query.all()
        result_list = []
        for recipe in recipes:
            json_recipe = recipe.get_json()
            if json_recipe is not None:
                result_list.append(json_recipe)
        return result_list


    @recipe_namespace.expect(serial_recipe)
    def post(self):
        """
        Create a new recipe using components that have already been created.
        The JSON Request object will contain only the IDs of all the connecting components.
        """

        data = request.json
        recipe = create_simple_recipe(data)
        recipe_json = recipe.get_json()
        if recipe_json is None:
            abort(400, "The Recipe did not get created due to invalid values")
        return recipe_json, 201


@recipe_namespace.route('/<int:recipe_id>/sensors')
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
            list_of_sensors.append(sensor.get_json())

        return list_of_sensors
