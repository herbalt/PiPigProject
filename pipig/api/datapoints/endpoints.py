from flask import request, abort
from flask_restplus import Resource

from api.datapoints.business import create_datapoints, update_datapoints
from api.datapoints.serializers import serial_datapoints, serial_datapoints_detail, serial_datapoints_new, serial_points
from pipig.api import api as api_plus
from pipig.data_points.models import DataPoints

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


@datapoints_namespace.route('/<int:datapoints_id>/')
class DatapointsItems(Resource):

    @datapoints_namespace.marshal_with(serial_datapoints_detail)
    @datapoints_namespace.response(200, description='Successfully returned list of Datapoints')
    @datapoints_namespace.response(500, description='Unable to find Datapoints in Db')
    def get(self, datapoints_id):
        """
        Returns list of all the individual Datapoints for a Datapoints Object.
        """

        datapoints = DataPoints.get(datapoints_id)
        if datapoints is None:
            abort(500)
        return datapoints.get_json()

    @datapoints_namespace.marshal_with(serial_datapoints_detail)
    @datapoints_namespace.expect(serial_points)
    @datapoints_namespace.response(201, description='Successfully updated the Datapoints')
    @datapoints_namespace.response(400, description='Failed to update the Datapoints')
    @datapoints_namespace.response(500, description='Unable to find Datapoints in Db')
    def put(self, datapoints_id):
        """
        Updates the Datapoints Object Model based on a JSON object of Points
        Takes the request object and checks this JSON object against the object model. \n
        Adds, Deletes and Updates all the relevant DataPoint IDs based on the variances from the Difference Step.\n
        Return the Datapoints object with the updated values.
        """
        data = request.json
        return update_datapoints(datapoints_id, data)





