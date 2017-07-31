from flask_restplus import fields
from pipig.api import api
from pipig.api.binders.serializers import serial_binders, serial_appliance_binder_detail, serial_sensor_binder_detail

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




