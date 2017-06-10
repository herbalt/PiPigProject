try:
    import RPi.GPIO as GPIO
    PI_CONNECTED = True
except ImportError:
    import pipig.gpio.placeholders as GPIO
    PI_CONNECTED = False

GPIO.setmode(GPIO.BCM)