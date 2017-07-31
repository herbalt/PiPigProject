from flask_restplus import fields
from pipig.api import api

serial_gpio = api.model('GPIO', {
    'pin number': fields.Integer(required=True,
                                 description='The PiPig unique ID for the GPIO pin that is connected to the Sensor that receives readings'),
    'pin name': fields.String(required=False, description='The name of the GPIO Pin'),
    'pin position': fields.Integer(required=False, description='The position of the GPIO Pin on the Raspberry Pi')
})

serial_pi_simple = api.model('Raspberry PI',
                      {
                          'id': fields.Integer(readOnly=True, description='Unique ID for the Raspberry PI'),
                          'model': fields.String(required=True, desctiption='The Model name of the Raspberry PI')
                      }
                      )

serial_pi = api.model('Raspberry PI',
                      {
                          'id': fields.Integer(readOnly=True, description='Unique ID for the Raspberry PI'),
                          'model': fields.String(required=True, desctiption='The Model name of the Raspberry PI'),
                          'pi pins': fields.List(fields.Nested(serial_gpio, required=False, description='The associated GPIO pin to the Raspberry PI'))
                      }
                      )