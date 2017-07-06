from flask import request
from flask_restplus import Resource

from api.datapoints.business import create_datapoints, create_datapoint, update_datapoint
from api.datapoints.serializers import serial_datapoints, serial_datapoint, serial_datapoints_new, serial_datapoint_new_known_datapoints_id, serial_datapoint_update
from pipig.api import api as api_plus
from pipig.data_points.models import DataPoint, DataPoints

datapoints_namespace = api_plus.namespace('datapoints',
                                      description='Datapoints processors inputs to outputs within the PiPig chain')


@datapoints_namespace.route('/')
class Datapoints(Resource):
    @datapoints_namespace.marshal_with(serial_datapoints)
    @datapoints_namespace.response(200, description='Successfully returned list of Datapoints', model=serial_datapoints)
    def get(self):
        """
        Returns list of all Datapoints stored in the Database without the individual Datapoints
        :return: list of JSON Datapoints objects
        """
        datapoints = DataPoints.query.all()
        return datapoints

    @datapoints_namespace.expect(serial_datapoints_new)
    @datapoints_namespace.response(201, description='Created a new Datapoints container', model=serial_datapoints)
    def post(self):
        """
        Create a new Datapoints container
        """
        data = request.json
        datapoints_id = create_datapoints(data)
        return datapoints_id, 201


@datapoints_namespace.route('<int:datapoints_id>/datapoint/')
class Datapoint(Resource):
    @datapoints_namespace.marshal_with(serial_datapoint)
    @datapoints_namespace.response(200, description='Successfully returned list of Datapoints', model=serial_datapoint)
    def get(self, datapoints_id):
        """
        Returns list of all the individual Datapoints for a Datapoints Object.
        :return: list of JSON Datapoint objects
        """

        datapoints = DataPoints.get(datapoints_id)
        return datapoints.get_points()

    @datapoints_namespace.expect(serial_datapoint_new_known_datapoints_id)
    @datapoints_namespace.marshal_with(serial_datapoint)
    @datapoints_namespace.response(201, description='Created a new Datapoint', model=serial_datapoint)
    def post(self, datapoints_id):
        """
        Create a new Datapoint for a Datapoints container
        """
        data = request.json
        datapoint = create_datapoint(datapoints_id, data)
        return datapoint, 201

    @datapoints_namespace.expect(serial_datapoint_update)
    @datapoints_namespace.response(201, description='Updated an existing Datapoint', model=serial_datapoint)
    def put(self, datapoints_id):
        """
        Update an existing Datapont for a Datapoints Container
        """
        data = request.json
        datapoint = update_datapoint(datapoints_id, data)

        return datapoint, 201



