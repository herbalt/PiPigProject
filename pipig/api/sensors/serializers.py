from flask_restplus import fields
from pipig.api import api

"""
serial_sensor = api.model('Sensor',  {
    'id': fields.Integer(readOnly=True, description='Unique ID for the Sensor'),
    'type_id': fields.Integer(required=True, description='The unique ID for the Type of Sensor'),
    'name': fields.String(required=True, description='The name of the Sensor'),
    'interval_between_readings': fields.Float(description='The time difference in seconds that the Sensor will take its readings'),
    'gpio_pin_id': fields.Integer(default=None, description='The PiPig unique ID for the GPIO pin that is connected to the Sensor to take readings')
})
"""

serial_new_sensor = api.model('Sensor creation parameters', {
    'type_id': fields.Integer(required=True, description='Unique ID for the Type of Sensor'),
    'name': fields.String(required=True, description='The name of the Sensor'),
    'interval_between_readings': fields.Float(description='The time difference in seconds that the Sensor will take its readings'),
    'gpio_pin_id': fields.Integer(default=None, description='The PiPig unique ID for the GPIO pin that is connected to the Sensor to take readings')
})


serial_sensor = api.model('Sensor',  {
    'id': fields.Integer(readOnly=True, description='Unique ID for the Sensor'),
    'type': fields.Nested(api.model('Sensor Type', {
        'id': fields.Integer(readOnly=True, description='Unique ID for the Sensor Type'),
        'name': fields.Integer(required=True, description='The name of the Sensor Type'),
        'units': fields.Nested(api.model('Sensor Units', {
            'id': fields.Integer(readOnly=True, description='Unique ID for the Unit'),
            'name': fields.String(required=True, description='The name of the Unit'),
            'display': fields.String(required=True, description='The characters to represent the units to use in the display')
        }))
    })),
    'name': fields.String(required=True, description='The name of the Sensor'),
    'gpio': fields.Nested(api.model('Sensor GPIO', {
        'pin number': fields.Integer(required=True, description='The PiPig unique ID for the GPIO pin that is connected to the Sensor that receives readings'),
        'pin name': fields.String(required=False, description='The name of the GPIO Pin')
    })),

})

