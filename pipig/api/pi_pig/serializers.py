
"""
Recipe
Raspberry PI
Session
"""
from flask_restplus import fields
from pipig.api import api
from pipig.api.sensors.serializers import serial_sensor
from pipig.api.recipes.serializers import serial_recipe
from pipig.api.raspberry_pi.serializers import serial_pi_simple
from pipig.api.general.serializers import serial_session

serial_pipig = api.model('PiPig',
                         {
                            'id': fields.Integer(readOnly=True, description='Unique ID for PiPig'),
                             'recipe': fields.Nested(serial_recipe, description='The Recipe used for the Pipig Instance'),
                             'raspberry pi': fields.Nested(serial_pi_simple, description='The Raspberry Pi Model used for the PiPig Instance'),
                             'session': fields.Nested(serial_session, description='The Session used for the PiPig Instance'),
                             'status': fields.String(required=False, description='The current Status of the PiPig Operation')
                        }
                         )

serial_pipig_config = api.model('PiPig Config',
                                {
                                  'recipe id': fields.Integer(required=True, description=''),
                                  'session name': fields.String(required=False, description=''),
                                  'raspberry pi id': fields.Integer(required=True, desciption='')

                              }
                                )


serial_sensor_snapshot = api.model('PiPig Sensor Snapshot',
                                   {
                                       'sensor': fields.Nested(serial_sensor)
                                   }

                                   )

serial_pipig_snapshot = api.model('PiPig Snapshot',
                                  {
                                    'id': fields.Integer(readOnly=True, description='Unique ID for PiPig'),
                                    'sensors': fields.Nested(serial_sensor_snapshot)
                                    }
                                  )

serial_pipig_status_input = api.model('PiPig Status Input',
                                      {
                                    'code': fields.Integer(readOnly=True, description='The ID of the PiPig Status')
                                }
                                      )

serial_pipig_status_name = api.model('PiPIg Status Name', {'name': fields.String(readOnly=True, description='The Name of the PiPig Status')})

serial_pipig_status = api.inherit('PiPig Status Input', serial_pipig_status_input, serial_pipig_status_name)