from flask import request
from flask_restplus import abort
from flask_restplus import Resource

from pipig.api.recipes.business import create_recipe, create_recipe_from_tuples, get_recipe_detail
from pipig.api.recipes.serializers import serial_recipe, serial_recipe_detail
from pipig.api.sensors.serializers import serial_sensor
from pipig.api.appliances.serializers import serial_appliance
from pipig.api.datapoints.serializers import serial_datapoints_detail
from pipig.api import api as api_plus
from recipes.models import Recipe
from sensors.models import Sensor
from appliances.models import Appliance
from data_points.models import DataPoints

recipe_namespace = api_plus.namespace('recipes',
                                      description='Instructions for a monitored and controlled Charcuterie Chamber operation')


@recipe_namespace.route('/')
class RecipeItems(Resource):

    @recipe_namespace.marshal_with(serial_recipe)
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

    @recipe_namespace.marshal_with(serial_recipe)
    @recipe_namespace.expect(serial_recipe)
    def post(self):
        """
        Create a new recipe.
        All objects IDs used in Recipe require them to already exist in the Database.
        The JSON Request object will contain only the IDs of all the connecting components.
        """

        data = request.json
        recipe = create_recipe(data)
        recipe_json = recipe.get_json()
        if recipe_json is None:
            abort(400, "The Recipe did not get created due to invalid values")
        return recipe_json, 201


@recipe_namespace.route('/<int:recipe_id>')
class RecipeDetail(Resource):

    @recipe_namespace.marshal_list_with(serial_recipe_detail)
    def get(self, recipe_id):
        """
        Retrieve all the details of all the Objects associated with the Recipe.
        Contains Sensor and Appliance Binders with the details of the components in detail
        :param recipe_id:
        :return:
        """
        recipe = Recipe.get(recipe_id)
        recipe_json = get_recipe_detail(recipe)
        return recipe_json


@recipe_namespace.route('/<int:recipe_id>/sensors')
class RecipeSensorItems(Resource):

    @recipe_namespace.marshal_list_with(serial_sensor)
    @recipe_namespace.response(code=200, description='The list of JSON sensors that relate to a Recipe')
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


@recipe_namespace.route('/<int:recipe_id>/appliances')
class RecipeApplianceItems(Resource):

    @recipe_namespace.marshal_list_with(serial_appliance)
    @recipe_namespace.response(code=200, description='The list of JSON Appliances that relate to a Recipe')
    def get(self, recipe_id):
        """
        Get all the Appliances that are associated with a particular recipe
        """

        recipe = Recipe.get(recipe_id)
        appliance_ids = recipe.get_appliance_ids()
        list_of_appliances = []

        for appliance_id in appliance_ids:
            appliance = Appliance.get(appliance_id)
            list_of_appliances.append(appliance.get_json())

        return list_of_appliances


@recipe_namespace.route('/<int:recipe_id>/datapoints')
class RecipeDatapointsItems(Resource):
    @recipe_namespace.marshal_list_with(serial_datapoints_detail)
    @recipe_namespace.response(code=200, description='The list of JSON Datapoints that relate to a Recipe')
    def get(self, recipe_id):
        """
        Get all the Datapoints that are associated with a particular recipe
        """
        recipe = Recipe.get(recipe_id)
        datapoints_ids = recipe.get_datapoints_ids()
        list_of_datapoints = []

        for datapoints_id in datapoints_ids:
            datapoint = DataPoints.get(datapoints_id)
            list_of_datapoints.append(datapoint.get_json())

        return list_of_datapoints