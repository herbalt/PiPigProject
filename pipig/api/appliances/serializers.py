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


