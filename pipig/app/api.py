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
from flask import Response, Request
from pipig import app


@app.route('/add_sensor', methods=['POST'])
def add_sensor():
    if Request.method == 'POST':
        pass


@app.route('/get_sensor/<int:key>', methods=['GET'])
def get_sensor(key):
    if Request.method == 'GET':
        pass


@app.route('/edit_sensor/<int:key>', methods=['POST'])
def edit_sensor(key):
    if Request.method == 'POST':
        pass


@app.route('/add_appliance', methods=['POST'])
def add_appliance():
    if Request.method == 'POST':
        pass


@app.route('/get_appliance/<int:key>', methods=['GET'])
def get_appliance(key):
    if Request.method == 'GET':
        pass


@app.route('/edit_appliance/<int:key>', methods=['POST'])
def edit_appliance(key):
    if Request.method == 'POST':
        pass


@app.route('/add_datapoints', methods=['POST'])
def add_datapoints():
    if Request.method == 'POST':
        pass


@app.route('/get_datapoints/<int:key>', methods=['GET'])
def get_datapoints(key):
    if Request.method == 'GET':
        pass


@app.route('/edit_datapoints/<int:key>', methods=['POST'])
def edit_datapoints(key):
    if Request.method == 'POST':
        pass


@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    if Request.method == 'POST':
        pass


@app.route('/get_recipe/<int:key>', methods=['GET'])
def get_recipe(key):
    if Request.method == 'GET':
        pass


@app.route('/edit_recipe/<int:key>', methods=['POST'])
def edit_recipe(key):
    if Request.method == 'POST':
        pass
    

@app.route('/get_sensor_readings/<int:recipe>/<int:sensor>/<float:start_time_elapsed>/<float:end_time_elapsed', methods=['GET'])
def get_sensor_readings(recipe, sensor, start_time_elapsed=None, end_time_elapsed=None):
    if Request.method == 'GET':
        pass





