try:
    import RPi.GPIO as GPIO
    PI_CONNECTED = True
except ImportError:
    import pi_gpio.GPIO_Placeholder as GPIO
    PI_CONNECTED = False

GPIO.setmode(GPIO.BCM)

