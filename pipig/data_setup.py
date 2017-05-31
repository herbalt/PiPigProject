import appliances.data_setup as appliances
import gpio_pins.data_setup as gpio_pins
import sensors.data_setup as sensors
import units.data_setup as generics
from pipig import app


def data_setup():
    sensors.data_setup()
    appliances.data_setup()
    generics.data_setup()
    gpio_pins.data_setup()
    # users.data_setup()

if __name__ == '__main__':
    with app.app_context():
        data_setup()

