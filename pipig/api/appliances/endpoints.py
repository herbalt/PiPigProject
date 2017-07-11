from flask import request
from flask_restplus import Resource

from api.appliances.business import create_appliance, update_appliance, get_appliance
from api.appliances.serializers import serial_appliance, serial_new_appliance
from api.appliances.parsers import update_appliance_parser
from pipig.api import api as api_plus
from pipig.appliances.models import Appliance

appliance_namespace = api_plus.namespace('appliances',
                                      description='Appliances are the output component within the PiPig chain, often GPIO or Console.')


@appliance_namespace.route('/')
class Appliances(Resource):
    @appliance_namespace.response(200, description='Successfully returned list of Appliances', model=serial_appliance)
    @appliance_namespace.response(500, description='Failed to retrieve Appliance list')
    def get(self):
        """
        Returns list of all Appliances stored in the Database.
        """
        appliances = Appliance.query.all()
        response_list = []
        for appliance in appliances:
            result = get_appliance(appliance)
            response_list.append(result)
        return response_list

    @appliance_namespace.expect(serial_new_appliance)
    @appliance_namespace.response(201, description='Created a new Appliance', model=serial_appliance)
    def post(self):
        """
        Create a new Appliance
        """
        data = request.json
        appliance = create_appliance(data)
        return get_appliance(appliance), 201


@appliance_namespace.route('/<int:appliance_id>')
@appliance_namespace.doc(params={'appliance_id': 'The Appliance ID to grab the Appliance JSON object'})
@appliance_namespace.response(500, 'Appliance not found')
class ApplianceItems(Resource):
    @appliance_namespace.response(code=200, description='The JSON of the specific Appliance', model=serial_appliance)
    def get(self, appliance_id):
        """
        Returns a Appliance related to a single Appliance ID
        :return: Appliance JSON Object
        """
        appliance = Appliance.query.filter(Appliance.id == appliance_id).one()
        return get_appliance(appliance)

    @appliance_namespace.expect(update_appliance_parser)
    def put(self, appliance_id):
        """
        Update a Appliance with new values.
        Any values with a None value will not be updated, except for GPIO which a Zero value will mean it is not updated
        """
        args = request.args
        appliance = update_appliance(appliance_id, args)
        return get_appliance(appliance), 201

    @appliance_namespace.response(code=200, description='The Appliance was successfully deleted from the Database')
    def delete(self, appliance_id):
        """
        Delete a Appliance from the Database.
        :return: The confirmation of the Appliance ID that was deleted
        """
        appliance = Appliance.query.filter(Appliance.id == appliance_id).one()
        appliance.delete()
        return {'Deleted Appliance': appliance_id}

