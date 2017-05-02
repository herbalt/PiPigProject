try:
    import RPi.GPIO as GPIO
    PI_CONNECTED = True
except ImportError:
    import placeholders as GPIO
    PI_CONNECTED = False

GPIO.setmode(GPIO.BCM)