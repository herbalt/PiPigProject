from flask_restplus import fields
from pipig.api import api

"""
The Models for the Data Point Objects
"""
serial_sensor_binder = api.model('Sensor Binder',  {
    'sensor id': fields.Integer(required=True, description='The Sensor ID to bind to a Datapoints Object'),
    'datapoint id': fields.Integer(required=True, description='The Datapoint ID to bind to a Sensor Object')
})

serial_appliance_binder = api.model('Appliance Binder', {
    'appliance id': fields.Integer(required=True, description='The Appliance ID to bind to a Datapoints Object'),
    'datapoint id': fields.Integer(required=True, description='The Datapoint ID to bind to a Appliance Object')
})

serial_sensor_bindings = api.model('Recipe Sensor Binders', {
'list of sensor bindings': fields.List(fields.Nested(serial_sensor_binder, required=False, description='The Datapoint objects associated with the Datapoint'))
})

serial_appliance_bindings = api.model('Recipe Appliance Binders', {
'list of appliance bindings': fields.List(
    fields.Nested(serial_appliance_binder, required=False, description='The Datapoint objects associated with the Datapoint')
)
})

"""
The Models for the Recipe Objects
"""
serial_recipe = api.model('Recipe',  {
    'name': fields.String(required=True, description='The name of the Recipe'),
    # 'list of sensor bindings': serial_sensor_bindings,
    # 'list of appliance bindings': serial_appliance_bindings
})



