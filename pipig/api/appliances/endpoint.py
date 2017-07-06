from flask import request
from flask_restplus import Resource

from api.appliances.business import create_appliance, update_appliance
from api.appliances.serializers import serial_appliance, serial_new_appliance
from pipig.api import api as api_plus
from pipig.appliances.models import Appliance

appliance_namespace = api_plus.namespace('appliances',
                                      description='Appliances are the output component within the PiPig chain, often GPIO or Console.')


@appliance_namespace.route('/')
class Appliances(Resource):
    @appliance_namespace.marshal_list_with(serial_appliance)
    @appliance_namespace.response(200, description='Successfully returned list of Appliances', model=serial_appliance)
    def get(self):
        """
        Returns list of all Appliances stored in the Database
        :return: list of JSON Appliance objects
        """
        # with app.app_context():
        appliances = Appliance.query.all()
        return appliances

    @appliance_namespace.expect(serial_new_appliance)
    @appliance_namespace.response(201, description='Created a new Appliance', model=serial_new_appliance)
    def post(self):
        """
        Create a new Appliance
        """
        data = request.json
        appliance_id = create_appliance(data)
        return appliance_id, 201


@appliance_namespace.route('/<int:appliance_id>')
@appliance_namespace.doc(params={'appliance_id': 'The Appliance ID to grab the Appliance JSON object'})
@appliance_namespace.response(500, 'Appliance not found')
class ApplianceItems(Resource):
    @appliance_namespace.marshal_with(serial_appliance)
    @appliance_namespace.response(code=200, description='The JSON of the specific Appliance', model=serial_appliance)
    def get(self, appliance_id):
        """
        Returns a Appliance related to a single Appliance ID
        :return: Appliance JSON Object
        """
        return Appliance.query.filter(Appliance.id == appliance_id).one()

    @appliance_namespace.marshal_with(serial_appliance)
    def post(self):
        """
        Update a Appliance with new values.
        Any values with a None value will not be updated, except for GPIO which a Zero value will mean it is not updated
        """
        data = request.json
        sensor_id = update_appliance(data)
        return sensor_id, 201

    @appliance_namespace.response(code=200, description='The Appliance was successfully deleted from the Database')
    def delete(self, appliance_id):
        """
        Delete a Appliance from the Database.
        :return: The confirmation of the Appliance ID that was deleted
        """
        sensor = Appliance.query.filter(Appliance.id == appliance_id).one()
        sensor.delete()
        return {'Deleted Appliance': appliance_id}

