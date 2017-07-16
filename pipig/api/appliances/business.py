from sqlalchemy.orm.exc import NoResultFound

from pipig.appliances.models import Appliance, ApplianceType
from pipig.generics.models import GenericUnits
from pipig.pi_gpio.models import GpioPin

def create_appliance(data):
    name = data.get('name')
    type_id = data.get('type_id')
    gpio_pin_id = data.get('gpio_pin_id')

    if gpio_pin_id == 0:
        gpio_pin_id = None

    # TODO Should add validation to this DB Entry
    appliance = Appliance.create(name=name, type_id=type_id, gpio_pin_id=gpio_pin_id)
    return appliance


def update_appliance(appliance_id, data):
    type_id = data.get('type_id')
    name = data.get('name')
    gpio_pin_id = data.get('gpio_pin_id')

    appliance = Appliance.get(appliance_id)
    # TODO Should add validation to these DB Entries
    if type_id is not None:
        appliance.update(type_id=type_id)

    if name is not None:
        appliance.update(name=name)

    if gpio_pin_id is not 0:
        appliance.update(gpio_pin_id=gpio_pin_id)

    return appliance.get_json()
