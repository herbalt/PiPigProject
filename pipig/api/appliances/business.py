from sqlalchemy.orm.exc import NoResultFound

from pipig.appliances.models import Appliance, ApplianceType
from pipig.generics.models import GenericUnits
from pipig.pi_gpio.models import GpioPin


def get_appliance(appliance_model):

    type_id = appliance_model.get_type_id()
    appliance_type = ApplianceType.query.filter(ApplianceType.id == type_id).one()
    units_id = appliance_type.get_units_id()
    units = GenericUnits.query.filter(GenericUnits.id == units_id).one()
    try:
        gpio_pin = GpioPin.query.filter(GpioPin.id == appliance_model.get_gpio_pin_id()).one()
    except NoResultFound:
        gpio_pin = GpioPin(None, None, None, 'No GPIO Connection')

    appliance_dict = {
        'appliance': {
            'id': appliance_model.get_id(),
            'name': appliance_model.get_name(),
            'appliance type': {
                'type id': appliance_type.get_id(),
                'type name': appliance_type.get_type(),
                'unit name': units.get_code_name(),
                'unit display name': units.get_display_units()
            },
            'gpio': {
                'pin number': gpio_pin.get_pin_number(),
                'pin name': gpio_pin.get_pin_name()
            }
        }
    }

    return appliance_dict


def create_appliance(data):
    name = data.get('name')
    type_id = data.get('type_id')
    gpio_pin_id = data.get('gpio_pin_id')

    if gpio_pin_id == 0:
        gpio_pin_id = None

    appliance = Appliance.create(name=name, type_id=type_id, gpio_pin_id=gpio_pin_id)
    return appliance


def update_appliance(appliance_id, data):
    type_id = data.get('type_id')
    name = data.get('name')
    gpio_pin_id = data.get('gpio_pin_id')

    appliance = Appliance.query.filter_by(id=appliance_id).one()
    if type_id is not None:
        appliance.update(type_id=type_id)

    if name is not None:
        appliance.update(name=name)

    if gpio_pin_id is not 0:
        appliance.update(gpio_pin_id=gpio_pin_id)

    return appliance
