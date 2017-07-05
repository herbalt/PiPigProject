from pipig.appliances.models import Appliance

def create_appliance(data):
    name = data.get('name')
    type_id = data.get('type_id')
    gpio_pin_id = data.get('gpio_pin_id')

    if gpio_pin_id == 0:
        gpio_pin_id = None

    appliance = Appliance(name=name, type_id=type_id, gpio_pin_id=gpio_pin_id)
    return appliance.get_id()
