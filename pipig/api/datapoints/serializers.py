from flask_restplus import fields
from pipig.api import api

"""
The Models for the Data Point Objects
"""
serial_datapoint = api.model('Datapoint',  {
    'id': fields.Integer(readOnly=True, description='Unique ID for the Datapoint'),
    'value': fields.Float(required=True, description='The reading value the Datapoint is set for at a given time'),
    'time elapsed': fields.Float(required=True, description='The time elapsed value the Datapoint')
})

serial_points = api.model('Points', {
'list of points': fields.List(fields.Nested(serial_datapoint, required=False, description='The Datapoint objects associated with the Datapoint'))
})

"""
The Models for the Datapoints Objects
"""
serial_datapoints = api.model('Datapoints',  {
    'id': fields.Integer(readOnly=True, description='Unique ID for the Datapoints'),
    'name': fields.String(required=True, description='The name of the Datapoints')
})

serial_datapoints_detail = api.model('Datapoints Detail',
                                     {
                                         'list of points': fields.List(fields.Nested(serial_datapoint, required=False, description='The Datapoint objects associated with the Datapoint')),
                                         'id': fields.Integer(readOnly=True, description='Unique ID for the Datapoints'),
                                        'name': fields.String(required=True, description='The name of the Datapoints')
                                     }
                                     )


serial_datapoints_new = api.model('New Datapoints',  {
    'name': fields.String(required=True, description='The name of the Datapoints')
})






