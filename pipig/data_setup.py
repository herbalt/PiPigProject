from pipig import app

import sensors.data_setup as sensors
import appliances.data_setup as appliances
import generics.data_setup as generics
import gpio_pins.data_setup as gpio_pins
import users.data_setup as users

def data_setup():
    sensors.data_setup()
    appliances.data_setup()
    generics.data_setup()
    gpio_pins.data_setup()
    # users.data_setup()

if __name__ == '__main__':
    with app.app_context():
        data_setup()

