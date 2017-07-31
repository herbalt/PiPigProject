from flask_restplus import fields
from pipig.api import api

serial_units = api.model('Units', {
    'id': fields.Integer(readOnly=True, description='Unique ID for the Unit'),
    'name': fields.String(required=True, description='The name of the Unit'),
    'display': fields.String(required=True, description='The characters to represent the units to use in the display')
})

serial_session = api.model('Session',
                           {
                               'id': fields.Integer(readOnly=True, description='Unique ID for the Session'),
                               'name': fields.String(required=True, description='The name of the Session'),
                               'start time': fields.Float(required=False, description='The time the Session started'),
                               'end time': fields.Float(required=False, description='The time the Session ended'),
                               'notes': fields.String(required=False, description='The notes taken about the Session')
                           }
                           )