from flask_restplus import reqparse

update_appliance_parser = reqparse.RequestParser()
update_appliance_parser.add_argument('type_id', type=int, help='The updated value for Appliance Type ID')
update_appliance_parser.add_argument('name', type=str, help='The updated value for name for the Appliance')
update_appliance_parser.add_argument('gpio_pin_id', type=int,  help='The updated value for GPIO Pin ID for the Appliance')


