from pipig.appliances.models import Appliance

def create_appliance(data):
    name = data.get('name')
    type_id = data.get('type_id')
    gpio_pin_id = data.get('gpio_pin_id')

    if gpio_pin_id == 0:
        gpio_pin_id = None

    appliance = Appliance.create(name=name, type_id=type_id, gpio_pin_id=gpio_pin_id)
    return appliance.get_id()


def update_appliance(data):
    appliance_id = data.get('sensor_id')
    type_id = data.get('type_id')
    name = data.get('name')
    gpio_pin_id = data.get('gpio_pin_id')


    if type_id is not None:
        Appliance.update(appliance_id=appliance_id, type_id=type_id)

    if name is not None:
        Appliance.update(appliance_id=appliance_id, name=name)

    if gpio_pin_id is not 0:
        Appliance.update(appliance_id=appliance_id, gpio_pin_id=gpio_pin_id)

    return Appliance.query.filter_by(id=appliance_id).one()