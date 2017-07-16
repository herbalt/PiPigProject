from flask import request, abort
from flask_restplus import Resource

from api.datapoints.business import create_datapoints, create_datapoint, update_datapoint
from api.datapoints.serializers import serial_datapoints, serial_datapoints_detail, serial_datapoints_new, serial_datapoint_new_known_datapoints_id, serial_datapoint_update
from pipig.api import api as api_plus
from pipig.data_points.models import DataPoint, DataPoints

datapoints_namespace = api_plus.namespace('datapoints',
                                      description='Datapoints processors inputs to outputs within the PiPig chain')

@datapoints_namespace.route('/')
class Datapoints(Resource):

    @datapoints_namespace.marshal_with(serial_datapoints)
    @datapoints_namespace.response(200, description='Successfully returned list of Datapoints')
    def get(self):
        """
        Returns list of all Datapoints stored in the Database without the individual Datapoints.
        """

        datapoints = DataPoints.query.all()
        result_list = []
        for datapoint in datapoints:
            result = datapoint.get_json()
            if result is not None:
                result_list.append(result)
        return result_list, 200


    @datapoints_namespace.marshal_with(serial_datapoints)
    @datapoints_namespace.expect(serial_datapoints_new)
    @datapoints_namespace.response(201, description='Created a new Datapoints container')
    def post(self):
        """
        Create a new Datapoints container
        """
        data = request.json
        datapoints = create_datapoints(data)
        return datapoints.get_json(), 201


@datapoints_namespace.route('<int:datapoints_id>/')
class DatapointsItems(Resource):

    @datapoints_namespace.marshal_with(serial_datapoints_detail)
    @datapoints_namespace.response(200, description='Successfully returned list of Datapoints')
    @datapoints_namespace.response(500, description='Unable to find Datapoints in Db')
    def get(self, datapoints_id):
        """
        Returns list of all the individual Datapoints for a Datapoints Object.
        :return: list of JSON Datapoint objects
        """

        datapoints = DataPoints.get(datapoints_id)
        if datapoints is None:
            abort(500)
        return datapoints.get_json()





