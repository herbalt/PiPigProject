from pipig import app
from factories.factory import APPLIANCE_TYPE_NAME_BASIC, APPLIANCE_TYPE_NAME_RELAY
from appliances.models import ApplianceType, Appliance


def data_setup():
    with app.app_context():
        print str(setup_appliance_type())
        print str(setup_testing_appliance())


def setup_appliance_type():
    appliance_ids = []
    appliance_ids.append(helper_setup_appliance_type(APPLIANCE_TYPE_NAME_BASIC, 5))
    appliance_ids.append(helper_setup_appliance_type(APPLIANCE_TYPE_NAME_RELAY, 5))
    return appliance_ids


def setup_testing_appliance():
    appliance_ids = []
    appliance_ids.append(helper_setup_appliances(APPLIANCE_TYPE_NAME_BASIC, "TEST_APPLIANCE"))
    appliance_ids.append(helper_setup_appliances(APPLIANCE_TYPE_NAME_RELAY, "RELAY_APPLIANCE"))
    return appliance_ids


def helper_setup_appliance_type(factory_constant, units_id):
    appliance_type = ApplianceType.query.filter_by(type_name=factory_constant).first()
    appliance_type_id = None
    if appliance_type is None:
        appliance_type_obj = ApplianceType.create(type_name=factory_constant, units_id=units_id)
        appliance_type_id = appliance_type_obj.get_id()
    return appliance_type_id


def helper_setup_appliances(factory_type_constant, appliance_name, gpio_pin_id=None):
    appliance = Appliance.query.filter_by(name=appliance_name).first()
    appliance_id = None
    if appliance is None:
        # TODO This might need to be more selective of what type object it is trying to find
        appliance_type = ApplianceType.query.filter_by(type_name=factory_type_constant).first()
        appliance_obj = Appliance.create(name=appliance_name, type_id=appliance_type.get_id(), gpio_pin_id=gpio_pin_id)
        appliance_id = appliance_obj.get_id()
    return appliance_id

if __name__ == '__main__':
    data_setup()