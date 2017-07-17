from flask import request, abort
from flask_restplus import Resource
from flask_restplus import abort

from api.sensors.business import create_sensor, update_sensor
from api.sensors.serializers import serial_sensor, serial_new_sensor
from pipig.api import api as api_plus
from pipig.sensors.models import Sensor
from pipig.api.sensors.parsers import update_sensor_parser

sensor_namespace = api_plus.namespace('sensors',
                                      description='A Sensor sends readings through the PiPig chain')


@sensor_namespace.route('/')
class Sensors(Resource):
    @sensor_namespace.marshal_list_with(serial_sensor)
    @sensor_namespace.response(200, description='Returned a list of sensors')
    @sensor_namespace.response(500, description='Failed to retrieve Sensor list, check if all component IDs exist')
    def get(self):
        """
        Returns list of all Sensors stored in the Database.
        The JSON Object will contain all the Nested Fields from all the Sensors.
        """
        sensors = Sensor.query.all()
        result_list = []
        for sensor in sensors:
            json_sensor = sensor.get_json()
            if json_sensor is not None:
                result_list.append(json_sensor)
        return result_list, 200

    @sensor_namespace.marshal_with(serial_sensor)
    @sensor_namespace.expect(serial_new_sensor)
    @sensor_namespace.response(201, description='Created a new Sensor')
    @sensor_namespace.response(400, description='The sensor cannot be created')
    def post(self):
        """
        Create a new Sensor.
        The JSON Object will contain all the Nested Fields from the new Sensor.
        """
        data = request.json
        sensor = create_sensor(data)
        sensor = sensor.get_json()
        if sensor is None:
            abort(400, "The sensor did not get created due to invalid values")
        return sensor, 201


@sensor_namespace.route('/<int:sensor_id>')
@sensor_namespace.doc(params={'sensor_id': 'The Sensor ID to grab the Sensor JSON object'})
class SensorItems(Resource):

    @sensor_namespace.marshal_with(serial_sensor)
    @sensor_namespace.response(code=200, description='The JSON of the specific Sensor')
    @sensor_namespace.response(code=400, description='The Sensor conponents are incorrect')
    @sensor_namespace.response(code=500, description='The Sensor does not exist')
    def get(self, sensor_id):
        """
        Returns a Sensor related to a single Sensor ID.
        The JSON Object will contain all the Nested Fields from the Sensor.
        """
        sensor = Sensor.get(sensor_id)
        if sensor is None:
            abort(500, 'The sensor ID does not exist in the Database')
        result = sensor.get_json()
        if result is None:
            abort(400, 'The sensor components cannot be built as Type or Units IDs are out of bounds')
        return result

    @sensor_namespace.expect(update_sensor_parser)
    @sensor_namespace.response(code=201, description='The Sensor JSON object in its amended form')
    @sensor_namespace.response(code=400, description='The parameters are invalid to build this sensor')
    @sensor_namespace.response(code=500, description='The Sensor ID does not exist in the Database')
    def put(self, sensor_id):
        """
        Update a Sensor with new values.
        Any values with a None value will not be updated, except for GPIO which a Zero value will mean it is not updated
        """
        args = request.args
        sensor_exists = Sensor.get(sensor_id)
        if sensor_exists is None:
            abort(500, 'The Sensor ID [%d] does not exist in the Database' % sensor_id)
        sensor = update_sensor(sensor_id, args)
        if sensor is None:
            return args, 400
        return sensor, 201

    @sensor_namespace.response(code=200, description='The Sensor was successfully deleted from the Database')
    @sensor_namespace.response(code=500, description='The Sensor does not exist')
    def delete(self, sensor_id):
        """
        Delete a Sensor from the Database.
        Historic Data may fail if a Sensor was used in historic operation. \n
        Returns the confirmation of the sensor ID that was deleted
        """
        sensor = Sensor.get(sensor_id)
        if sensor is None:
            abort(500, 'The Sensor ID [%d] does not exist in the Database to allow it to be deleted from the Database' % sensor_id)
        sensor.delete()
        return {'Deleted Sensor': sensor_id}, 200

