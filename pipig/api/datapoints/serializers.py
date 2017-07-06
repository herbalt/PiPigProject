from flask_restplus import fields
from pipig.api import api


serial_datapoints = api.model('Datapoints',  {
    'id': fields.Integer(readOnly=True, description='Unique ID for the Datapoints'),
    'name': fields.String(required=True, description='The name of the Datapoints')
})

serial_datapoints_new = api.model('New Datapoints',  {
    'name': fields.String(required=True, description='The name of the Datapoints')
})

serial_datapoint = api.model('Datapoint',  {
    'id': fields.Integer(readOnly=True, description='Unique ID for the Datapoint'),
    'data_points_id': fields.Integer(required=True, description='The ID for the Datapoints this point is associated with'),
    'value': fields.Float(required=True, description='The reading value the Datapoint is set for at a given time'),
    'time_elapsed': fields.Float(required=True, description='The time elapsed value the Datapoint')
})

serial_datapoint_update = api.model('Update existing Datapoint',  {
    'id': fields.Integer(readOnly=True, description='Unique ID for the Datapoint'),
    'value': fields.Float(required=True, description='The reading value the Datapoint is set for at a given time'),
    'time_elapsed': fields.Float(required=True, description='The time elapsed value the Datapoint')
})

serial_datapoint_new_known_datapoints_id = api.model('New Datapoint values',  {
    'value': fields.Float(required=True, description='The reading value the Datapoint is set for at a given time'),
    'time_elapsed': fields.Float(required=True, description='The time elapsed value the Datapoint')
})


