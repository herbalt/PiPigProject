from pipig import app
from pipig.factories.factory import APPLIANCE_TYPE_NAME_BASIC
from pipig.appliances.models import ApplianceType, Appliance

def data_setup():
    with app.app_context():
        setup_appliance_type()
        setup_testing_appliance()


def setup_appliance_type():
    appliance = Appliance.query.filter_by(name=APPLIANCE_TYPE_NAME_BASIC).first()
    if appliance is None:
        ApplianceType.create(name=APPLIANCE_TYPE_NAME_BASIC, units_id=5)
    return True


def setup_testing_appliance():
    appliance = Appliance.query.filter_by(name='TEST_APPLIANCE').first()
    if appliance is None:
        Appliance.create(name='TEST_APPLIANCE', type_id=1)
    return True



if __name__ == '__main__':
    data_setup()