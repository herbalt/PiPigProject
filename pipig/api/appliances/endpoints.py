from flask import request, abort
from flask_restplus import Resource

from api.appliances.business import create_appliance, update_appliance
from api.appliances.serializers import serial_appliance, serial_new_appliance
from api.appliances.parsers import update_appliance_parser
from pipig.api import api as api_plus
from pipig.appliances.models import Appliance

appliance_namespace = api_plus.namespace('appliances',
                                      description='Appliances are the output component within the PiPig chain, often GPIO or Console.')


@appliance_namespace.route('/')
class Appliances(Resource):

    @appliance_namespace.marshal_list_with(serial_appliance)
    @appliance_namespace.response(200, description='Successfully returned list of Appliances')
    @appliance_namespace.response(500, description='Failed to retrieve Appliance list')
    def get(self):
        """
        Returns list of all Appliances stored in the Database.
        The List of JSON Objects containing all the Nested Fields from the Appliance.
        """
        appliances = Appliance.query.all()
        result_list = []
        for appliance in appliances:
            result = appliance.get_json()
            if result is not None:
                result_list.append(result)
        return result_list, 200

    @appliance_namespace.expect(serial_new_appliance)
    @appliance_namespace.marshal_with(serial_appliance)
    @appliance_namespace.response(201, description='Created a new Appliance')
    @appliance_namespace.response(400, description='The Appliance cannot be created')
    def post(self):
        """
        Create a new Appliance.
        The JSON Object will contain all the Nested Fields from the Appliance.
        """
        data = request.json
        appliance = create_appliance(data)
        appliance = appliance.get_json()
        if appliance is None:
            abort(400, "The Appliance did not get created due to invalid values")
        return appliance, 201


@appliance_namespace.route('/<int:appliance_id>')
@appliance_namespace.doc(params={'appliance_id': 'The Appliance ID to grab the Appliance JSON object'})
class ApplianceItems(Resource):

    @appliance_namespace.marshal_with(serial_appliance)
    @appliance_namespace.response(code=200, description='The JSON of the specific Appliance')
    @appliance_namespace.response(code=400, description='The Appliance conponents are incorrect')
    @appliance_namespace.response(code=500, description='The Appliance does not exist')
    def get(self, appliance_id):
        """
        Returns a Appliance related to a single Appliance ID.
        The JSON Object will contain all the Nested Fields from the Appliance.
        """
        appliance = Appliance.get(appliance_id)
        if appliance is None:
            abort(500, 'The Appliance ID does not exist in the Database')
        result = appliance.get_json()
        if result is None:
            abort(400, 'The Appliance components cannot be built as Type or Units IDs are out of bounds')
        return appliance.get_json()

    @appliance_namespace.expect(update_appliance_parser)
    @appliance_namespace.response(code=201, description='The Appliance JSON object in its amended form')
    @appliance_namespace.response(code=400, description='The parameters are invalid to build this Appliance')
    @appliance_namespace.response(code=500, description='The Appliance ID does not exist in the Database')
    def put(self, appliance_id):
        """
        Update a Appliance with new values.
        Any values with a None value will not be updated, except for GPIO which a Zero value will mean it is not updated
        """
        args = request.args
        appliance_exists = Appliance.get(appliance_id)
        if appliance_exists is None:
            abort(500, 'The Appliance ID [%d] does not exist in the Database' % appliance_id)
        appliance = update_appliance(appliance_id, args)
        if appliance is None:
            return args, 400
        return appliance, 201

    @appliance_namespace.response(code=200, description='The Appliance was successfully deleted from the Database')
    @appliance_namespace.response(code=500, description='The Appliance does not exist')
    def delete(self, appliance_id):
        """
        Delete a Appliance from the Database.
        :return: The confirmation of the Appliance ID that was deleted
        """
        appliance = Appliance.get(appliance_id)
        if appliance is None:
            abort(500, 'The Appliance ID [%d] does not exist in the Database to allow it to be deleted from the Database' % appliance_id)
        appliance.delete()
        return {'Deleted Appliance': appliance_id}

