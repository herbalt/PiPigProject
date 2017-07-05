from flask_restplus import fields
from pipig.api import api


serial_sensor = api.model('Sensor',  {
    'id': fields.Integer(readOnly=True, description='Unique ID for the Sensor'),
    'type_id': fields.Integer(required=True, description='The unique ID for the Type of Sensor'),
    'name': fields.String(required=True, description='The name of the Sensor'),
    'interval_between_readings': fields.Float(description='The time difference in seconds that the Sensor will take its readings'),
    'gpio_pin_id': fields.Integer(default=None, description='The PiPig unique ID for the GPIO pin that is connected to the Sensor to take readings')
})

serial_new_sensor = api.model('Sensor creation parameters', {
    'type_id': fields.Integer(required=True, description='Unique ID for the Type of Sensor'),
    'name': fields.String(required=True, description='The name of the Sensor'),
    'interval_between_readings': fields.Float(description='The time difference in seconds that the Sensor will take its readings'),
    'gpio_pin_id': fields.Integer(default=None, description='The PiPig unique ID for the GPIO pin that is connected to the Sensor to take readings')
})
