try:
    import RPi.GPIO as GPIO
    PI_CONNECTED = True
except ImportError:
    import pi_gpio.GPIO_Mock as GPIO
    PI_CONNECTED = False

GPIO.setmode(GPIO.BCM)

def gpio_configure_sensors(sensor_dict):
    for item_id in sensor_dict:
        gpio_pin = sensor_dict[item_id].get_gpio_pin()
        if gpio_pin is not None:
            GPIO.setup(gpio_pin=gpio_pin, direction=GPIO.IN)


def gpio_configure_appliances(appliance_dict):
    for item_id in appliance_dict:
        gpio_pin = appliance_dict[item_id].get_gpio_pin()
        if gpio_pin is not None:
            GPIO.setup(gpio_pin=gpio_pin, direction=GPIO.OUT)

def gpio_configure_application(sensor_dict, appliance_dict):
    gpio_configure_sensors(sensor_dict)
    gpio_configure_appliances(appliance_dict)
