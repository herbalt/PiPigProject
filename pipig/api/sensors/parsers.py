from flask_restplus import reqparse

"""
Constructs the Arguments to Update a Sensor with new Parameters
"""
update_sensor_parser = reqparse.RequestParser()
update_sensor_parser.add_argument('type_id', type=int, help='The updated value for Sensor Type ID')
update_sensor_parser.add_argument('name', type=str, help='The updated value for name for the Sensor')
update_sensor_parser.add_argument('gpio_pin_id', type=int, help='The updated value for GPIO Pin ID for the Sensor')
update_sensor_parser.add_argument('interval_between_readings', type=float, help='The time to pass in seconds between each sensor reading')
