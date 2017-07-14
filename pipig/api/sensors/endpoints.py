"""
This is the Endpoint Summary for PiPig

What do people what to do and achieve?

USER STORIES
* As a User I would like to create and edit sensors in a browser
* As a User I would like to create and edit appiances in a browser
* As a User I would like to define and edit a series of datapoints that thresholds of readings will interact with
As a User I would like to start a new session with a specific recipe
* As a User I would like to be able to combine sensors, appliances and datapoints to create a Recipe
As a User I would like to be able to view the streaming set of sensor readings for a running and archived session
As a User I would like to be able to view the streaming set of appliance interactions for a running and archived session
"""
from flask import request, abort
from flask_restplus import Resource
from sqlalchemy.orm.exc import NoResultFound
from flask_restplus import abort

from api.sensors.business import create_sensor, update_sensor
from api.sensors.serializers import serial_sensor, serial_new_sensor
from pipig.api import api as api_plus
from pipig.sensors.models import Sensor, SensorType
from pipig.api.sensors.business import get_sensor
from pipig.api.sensors.parsers import update_sensor_parser

sensor_namespace = api_plus.namespace('sensors',
                                      description='A Sensor sends readings through the PiPig chain')


@sensor_namespace.route('/')
class Sensors(Resource):
    # @sensor_namespace.marshal_list_with(serial_sensor)
    @sensor_namespace.doc(serial_sensor)
    @sensor_namespace.response(200, description='Successfully returned list of sensors', model=serial_sensor)
    def get(self):
        """
        Returns list of all Sensors stored in the Database
        :return: list of JSON Sensor objects
        """
        # with app.app_context():
        sensors = Sensor.query.all()
        result_list = []
        for sensor in sensors:
            json_sensor = get_sensor(sensor)
            if json_sensor is not None:
                result_list.append(json_sensor)
        return result_list

    @sensor_namespace.expect(serial_new_sensor)
    @sensor_namespace.response(201, description='Created a new Sensor', model=serial_sensor)
    def post(self):
        """
        Create a new Sensor
        """
        data = request.json
        sensor = create_sensor(data)
        sensor = get_sensor(sensor)
        if sensor is None:
            abort(400, "The sensor did not get created due to invalid values")
        return sensor, 201


@sensor_namespace.route('/<int:sensor_id>')
@sensor_namespace.doc(params={'sensor_id': 'The Sensor ID to grab the Sensor JSON object'})
@sensor_namespace.response(500, 'Sensor not found')
class SensorItems(Resource):
    # @sensor_namespace.marshal_with(serial_sensor)
    @sensor_namespace.response(code=200, description='The JSON of the specific Sensor', model=serial_sensor)
    def get(self, sensor_id):
        """
        Returns a Sensor related to a single Sensor ID
        :return: Sensor JSON Object
        """
        sensor = Sensor.get(sensor_id)
        if sensor is None:
            abort(400, 'The sensor ID does not exist in the Database')
        result = get_sensor(sensor)
        if result is None:
            abort(400, 'The sensor components cannot be built as Type or Units IDs are out of bounds')
        return result

    @sensor_namespace.expect(update_sensor_parser)
    @sensor_namespace.response(code=201, description='The Sensor JSON object in its amended form')
    @sensor_namespace.response(code=400, description='The parameters are invalid to build this sensor', model=update_sensor_parser)
    def put(self, sensor_id):
        """
        Update a Sensor with new values.
        Any values with a None value will not be updated, except for GPIO which a Zero value will mean it is not updated
        """
        args = request.args

        sensor = update_sensor(sensor_id, args)
        if sensor is None:
            return args, 400
        return get_sensor(sensor), 201

    @sensor_namespace.response(code=200, description='The Sensor was successfully deleted from the Database')
    def delete(self, sensor_id):
        """
        Delete a Sensor from the Database. Historic Data may fail if a Sensor was used in historic operation.
        :return: The confirmation of the sensor ID that was deleted
        """
        sensor = Sensor.query.filter(Sensor.id == sensor_id).one()
        sensor.delete()
        return {'Deleted Sensor': sensor_id}

