from flask_restplus import fields
from pipig.api import api

"""
serial_units = api.models('Units', {
    'id': fields.Integer(readOnly=True, description='Unique ID for the Unit'),
    'name': fields.String(required=True, description='The name of the Unit'),
    'display': fields.String(required=True, description='The characters to represent the units to use in the display')
})

serial_appliance_type = api.models('Appliance Type', {
    'id': fields.Integer(readOnly=True, description='Unique ID for the Appliance Type'),
    'name': fields.Integer(required=True, description='The name of the Appliance Type'),
    'units': fields.Nested(serial_units)
})

serial_appliance = api.model('Appliance',  {
    'id': fields.Integer(readOnly=True, description='Unique ID for the Appliance'),
    'type': fields.Nested(serial_appliance_type),
    'name': fields.String(required=True, description='The name of the Appliance'),
    'gpio_pin_id': fields.Integer(default=None, description='The PiPig unique ID for the GPIO pin that is connected to the Appliance that receives readings')
})
"""
serial_appliance = api.model('Appliance',  {
    'id': fields.Integer(readOnly=True, description='Unique ID for the Appliance'),
    'type': fields.Nested(api.model('serial_appliance_type', {
        'id': fields.Integer(readOnly=True, description='Unique ID for the Appliance Type'),
        'name': fields.Integer(required=True, description='The name of the Appliance Type'),
        'units': fields.Nested(api.model('serial_units', {
            'id': fields.Integer(readOnly=True, description='Unique ID for the Unit'),
            'name': fields.String(required=True, description='The name of the Unit'),
            'display': fields.String(required=True, description='The characters to represent the units to use in the display')
        }))
    })),
    'name': fields.String(required=True, description='The name of the Appliance'),
    'gpio': fields.Nested(api.model('serial_gpio', {
        'pin number': fields.Integer(required=True, description='The PiPig unique ID for the GPIO pin that is connected to the Appliance that receives readings'),
        'pin name': fields.String(required=False, description='The name of the GPIO Pin')
    })),

})



serial_new_appliance = api.model('Appliance creation parameters', {
    'type_id': fields.Integer(required=True, description='Unique ID for the Type of Appliance'),
    'name': fields.String(required=True, description='The name of the Appliance'),
    'gpio_pin_id': fields.Integer(default=None, description='The PiPig unique ID for the GPIO pin that is connected to the Appliance that receives readings')
})


