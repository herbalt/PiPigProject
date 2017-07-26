from flask_restplus import fields
from pipig.api import api
from pipig.api.sensors.serializers import serial_sensor
from pipig.api.appliances.serializers import serial_appliance
from pipig.api.datapoints.serializers import serial_datapoints_detail

"""
The Models for the Data Point Objects
"""
serial_sensor_binder = api.model('Sensor Binder',  {
    'sensor id': fields.Integer(required=True, description='The Sensor ID to bind to a Datapoints Object'),
    'datapoint id': fields.Integer(required=True, description='The Datapoint ID to bind to a Sensor Object')
})



serial_sensor_binder_detail = api.model('Sensor Binder Detail', {
    'sensor': fields.Nested(serial_sensor, required=True, description='The Sensor object associated with the Binder'),
    'datapoint': fields.Nested(serial_datapoints_detail, required=True, description='The Datapoint Object associated with the Binder')
})

serial_appliance_binder_detail = api.model('Appliance Binder Detail',
                                           {
                                                'appliance': fields.Nested(serial_appliance, required=True, description='The Appliance object associated with the Binder'),
                                                'datapoint': fields.Nested(serial_datapoints_detail, required=True, description='The Datapoint Object associated with the Binder'),
                                                'polarity': fields.Integer(required=True, description='The Polarity of the Binder')
                                           }
                                           )

serial_appliance_binder = api.model('Appliance Binder', {
    'appliance id': fields.Integer(required=True, description='The Appliance ID to bind to a Datapoints Object'),
    'datapoint id': fields.Integer(required=True, description='The Datapoint ID to bind to a Appliance Object'),
    'polarity': fields.Integer(required=True, description='The Polarity of the Binder')
})

serial_sensor_bindings = api.model('Recipe Sensor Binders', {
'list of sensor bindings': fields.List(fields.Nested(serial_sensor_binder, required=False, description='The Datapoint objects associated with the Datapoint'))
})

serial_appliance_bindings = api.model('Recipe Appliance Binders',
                                      {
                                          'list of appliance bindings': fields.List(
                                              fields.Nested(serial_appliance_binder,
                                                            required=False,
                                                            description='The Datapoint objects associated with the Datapoint')
                                          )
                                      }
                                      )

"""
The Models for the Recipe Objects
"""

serial_binders = api.inherit('Binders', serial_sensor_bindings, serial_appliance_bindings)
serial_recipe_base = api.model('Recipe Name', {
    'name': fields.String(required=True, description='The name of the Recipe'),
    'recipe id': fields.Integer(required=True, description='The ID of the Recipe')
})
serial_recipe = api.inherit('Recipe', serial_binders, serial_recipe_base)




serial_recipe_detail = api.model('Recipe Detail',
                                 {
                                     'list of appliance bindings': fields.Nested(serial_appliance_binder_detail),
                                     'list of sensor bindings': fields.Nested(serial_sensor_binder_detail),
                                     'recipe base': fields.Nested(serial_recipe_base)
                                 }
                                 )




