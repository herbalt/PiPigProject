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
from flask import request
from flask_restplus import Resource

from api.sensors.business import create_sensor
from api.sensors.serializers import serial_sensor, serial_new_sensor
from pipig.api import api as api_plus
from pipig.sensors.models import Sensor

sensor_namespace = api_plus.namespace('sensors',
                                      description='API to access sensor details from the database')


@sensor_namespace.route('/')
class Sensors(Resource):
    @sensor_namespace.marshal_list_with(serial_sensor)
    @sensor_namespace.response(200, description='Successfully returned list of sensors', model=serial_sensor)
    def get(self):
        """
        Returns list of all Sensors stored in the Database
        :return: list of JSON Sensor objects
        """
        # with app.app_context():
        sensors = Sensor.query.all()
        return sensors

    @sensor_namespace.expect(serial_new_sensor)
    @sensor_namespace.response(201, description='Created a new Sensor', model=serial_new_sensor)
    def post(self):
        """
        Create a new Sensor
        """
        data = request.json
        sensor_id = create_sensor(data)
        return sensor_id, 201


@sensor_namespace.route('/<int:sensor_id>')
@sensor_namespace.doc(params={'sensor_id': 'The Sensor ID to grab the Sensor JSON object'})
@sensor_namespace.response(500, 'Sensor not found')
class SensorItems(Resource):
    @sensor_namespace.marshal_with(serial_sensor)
    @sensor_namespace.response(code=200, description='The JSON of the specific Sensor', model=serial_sensor)
    def get(self, sensor_id):
        """
        Returns a Sensor related to a single Sensor ID
        :param sensor_id:
        :return: Sensor JSON Object
        """
        return Sensor.query.filter(Sensor.id == sensor_id).one()




"""
@api.route('/edit_sensor/<int:key>', methods=['POST'])
def edit_sensor(key):
    if Request.method == 'POST':
        pass


@api.route('/add_appliance', methods=['POST'])
def add_appliance():
    if Request.method == 'POST':
        pass


@api.route('/get_appliance/<int:key>', methods=['GET'])
def get_appliance(key):
    if Request.method == 'GET':
        pass


@api.route('/edit_appliance/<int:key>', methods=['POST'])
def edit_appliance(key):
    if Request.method == 'POST':
        pass


@api.route('/add_datapoints', methods=['POST'])
def add_datapoints():
    if Request.method == 'POST':
        pass


@api.route('/get_datapoints/<int:key>', methods=['GET'])
def get_datapoints(key):
    if Request.method == 'GET':
        pass


@api.route('/edit_datapoints/<int:key>', methods=['POST'])
def edit_datapoints(key):
    if Request.method == 'POST':
        pass


@api.route('/add_recipe', methods=['POST'])
def add_recipe():
    if Request.method == 'POST':
        pass


@api.route('/get_recipe/<int:key>', methods=['GET'])
def get_recipe(key):
    if Request.method == 'GET':
        pass


@api.route('/edit_recipe/<int:key>', methods=['POST'])
def edit_recipe(key):
    if Request.method == 'POST':
        pass


@api.route('/get_sensor_readings/<int:recipe>/<int:serial_sensor>/<float:start_time_elapsed>/<float:end_time_elapsed', methods=['GET'])
def get_sensor_readings(recipe, serial_sensor, start_time_elapsed=None, end_time_elapsed=None):
    if Request.method == 'GET':
        pass

"""
