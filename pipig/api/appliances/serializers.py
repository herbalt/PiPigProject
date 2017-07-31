from flask_restplus import fields
from pipig.api import api
from pipig.api.raspberry_pi.serializers import serial_gpio
from pipig.api.general.serializers import serial_units
"""
NESTED JSON MODELS
"""

serial_appliance_type = api.model('Type', {
        'id': fields.Integer(readOnly=True, description='Unique ID for the Type of Object'),
        'type name': fields.String(required=True, description='The name of the Type of Object'),
        'Units': fields.Nested(serial_units)
})

"""
APPLIANCE JSON MODELS
"""
serial_new_appliance = api.model('Appliance creation parameters', {
    'type_id': fields.Integer(required=True, description='Unique ID for the Type of Appliance'),
    'name': fields.String(required=True, description='The name of the Appliance'),
    'gpio_pin_id': fields.Integer(default=None, description='The PiPig unique ID for the GPIO pin that is connected to the Appliance that receives readings')
})


serial_appliance = api.model('Appliance',  {
    'id': fields.Integer(readOnly=True, description='Unique ID for the Appliance'),
    'Appliance Type': fields.Nested(serial_appliance_type, required=True, description='The type of Sensor, for example: GPIO Appliance'),
    'name': fields.String(required=True, description='The name of the Sensor'),
    'Appliance GPIO': fields.Nested(serial_gpio, required=True, description='The GPIO connector for the Appliance'),
})


