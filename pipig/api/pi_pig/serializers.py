
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


serial_session = api.model('Session',
                           {
                               'id': fields.Integer(readOnly=True, description='Unique ID for the Session'),
                               'name': fields.String(required=True, description='The name of the Session'),
                               'start time': fields.Float(required=False, description='The time the Session started'),
                               'end time': fields.Float(required=False, description='The time the Session ended'),
                               'notes': fields.String(required=False, description='The notes taken about the Session')
                           }
                           )

serial_pipig = api.model('PiPig',
                         {
                            'id': fields.Integer(readOnly=True, description='Unique ID for PiPig'),
                             'recipe': fields.Nested(serial_recipe),
                             'raspberry pi': fields.Nested(serial_pi_simple),
                             'session': fields.Nested(serial_session),
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