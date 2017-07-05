from flask_restplus import fields
from pipig.api import api


serial_appliance = api.model('Appliance',  {
    'id': fields.Integer(readOnly=True, description='Unique ID for the Appliance'),
    'type_id': fields.Integer(required=True, description='The unique ID for the Type of Appliance'),
    'name': fields.String(required=True, description='The name of the Appliance'),
    'gpio_pin_id': fields.Integer(default=None, description='The PiPig unique ID for the GPIO pin that is connected to the Appliance that receives readings')
})

serial_new_appliance = api.model('Appliance creation parameters', {
    'type_id': fields.Integer(required=True, description='Unique ID for the Type of Appliance'),
    'name': fields.String(required=True, description='The name of the Appliance'),
    'gpio_pin_id': fields.Integer(default=None, description='The PiPig unique ID for the GPIO pin that is connected to the Appliance that receives readings')
})
