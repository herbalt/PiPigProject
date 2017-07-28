from flask_restplus import fields
from pipig.api import api




serial_pipig = api.model('PiPig',
                         {
                            'id': fields.Integer(readOnly=True, description='Unique ID for PiPig')
                        }
                         )

serial_pipig_config = api.model('PiPig Config',
                                {
                                  'recipe id': fields.Integer(required=True, description=''),
                                  'session name': fields.String(required=False, description=''),
                                  'raspberry pi id': fields.Integer(required=True, desciption='')

                              }
                                )

serial_pipig_snapshot = api.model('PiPig Snapshot',
                                  {
                                    'id': fields.Integer(readOnly=True, description='Unique ID for PiPig')
                              }
                                  )