from flask_restplus import fields
from pipig.api import api

"""
NESTED JSON MODELS
"""
serial_units = api.model('Units', {
            'id': fields.Integer(readOnly=True, description='Unique ID for the Unit'),
            'name': fields.String(required=True, description='The name of the Unit'),
            'display': fields.String(required=True, description='The characters to represent the units to use in the display')
})

serial_gpio = api.model('GPIO', {
        'pin number': fields.Integer(required=True, description='The PiPig unique ID for the GPIO pin that is connected to the Sensor that receives readings'),
        'pin name': fields.String(required=False, description='The name of the GPIO Pin'),
        'pin position': fields.Integer(required=False, description='The position of the GPIO Pin on the Raspberry Pi')
    })

serial_sensor_type = api.model('Type', {
        'id': fields.Integer(readOnly=True, description='Unique ID for the Type of Object'),
        'type name': fields.String(required=True, description='The name of the Type of Object'),
        'minimum refresh': fields.Float(description='The smallest time in seconds that a sensor type can tolerate'),
        'Units': fields.Nested(serial_units)
})

"""
SENSOR JSON MODELS
"""
serial_sensor = api.model('Sensor',  {
    'id': fields.Integer(readOnly=True, description='Unique ID for the Sensor'),
    'Sensor Type': fields.Nested(serial_sensor_type, required=True, description='The type of Sensor, for example: DHT22 Temperature Sensor'),
    'name': fields.String(required=True, description='The name of the Sensor'),
    'Sensor GPIO': fields.Nested(serial_gpio, required=True, description='The GPIO connector for the Sensor'),
    'interval between readings': fields.Float(required=True, description='The GPIO connector for the Sensor'),
})

serial_new_sensor = api.model('Sensor creation parameters', {
    'type_id': fields.Integer(required=True, description='Unique ID for the Type of Sensor'),
    'name': fields.String(required=True, description='The name of the Sensor'),
    'interval_between_readings': fields.Float(description='The time difference in seconds that the Sensor will take its readings'),
    'gpio_pin_id': fields.Integer(default=None, description='The PiPig unique ID for the GPIO pin that is connected to the Sensor to take readings')
})
