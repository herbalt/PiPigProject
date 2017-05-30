from appliances import data_setup as appliance_data
from generics import data_setup as generics_data
from gpio_pins import data_setup as gpio_data
from sensors import data_setup as sensor_data


def data_setup():
    appliance_data.data_setup()
    generics_data.data_setup()
    gpio_data.data_setup()
    sensor_data.data_setup()



