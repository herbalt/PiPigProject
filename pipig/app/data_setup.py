from pipig.appliances import data_setup as appliance_data
from pipig.gpio_pins import data_setup as gpio_data
from pipig.sensors import data_setup as sensor_data
from pipig.units import data_setup as generics_data
from pipig.users import data_setup as users_data


def data_setup():
    """

    :return:
    """
    appliance_data.data_setup()
    generics_data.data_setup()
    gpio_data.data_setup()
    sensor_data.data_setup()
    users_data.data_setup()

if __name__ == "__main__":
    data_setup()



