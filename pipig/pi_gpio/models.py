from pi_gpio import config
from pipig.data import db, CRUDMixin
from pi_gpio.GPIO_Placeholder import BCM, BOARD, HIGH, IN, LOW, OUT


class GpioPin(db.Model, CRUDMixin):
    __tablename__ = "gpio_pin"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    pin_position = db.Column(db.Integer, nullable=False)
    pin_number = db.Column(db.Integer, nullable=True)
    pin_name = db.Column(db.String)
    bcm_pin = db.Column(db.Integer, nullable=True)

    def __init__(self, pin_position, pin_number, bcm_pin, pin_name=""):
        # Set Parameters
        self.pin_position = pin_position
        self.pin_number = pin_number
        self.bcm_pin = bcm_pin
        self.pin_name = pin_name

        # Set State Defaults
        self.state = IN
        self.pupd = None
        self.event_detection = None
        self.value = LOW

    """
    GETTERS
    """
    def get_id(self):
        return self.id

    def get_pin_number(self):
        if config.GPIO.getmode() == "BCM":
            return self.bcm_pin
        else:
            return self.pin_number

    def get_pin_name(self):
        return self.pin_name

    def get_state(self):
        return self.state

    def get_pupd(self):
        return self.pupd

    def get_event_detection(self):
        return self.event_detection

    def get_value(self):
        return self.value

    """
    SETTERS
    """
    def set_state(self, state):
        if state is IN or OUT:
            self.state = state
        return self.get_state()

    def set_pupd(self, pupd):
        self.pupd = pupd
        return self.get_pupd()

    def set_event_detection(self, event_detection):
        self.event_detection = event_detection
        return self.get_event_detection()

    def set_value(self, value):
        if value is LOW or HIGH:
            self.value = value
        return self.value


class RaspberryPi(db.Model, CRUDMixin):

    __tablename__ = "raspberry_pi"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    pin_count = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String)

    def __init__(self, pin_count, name):
        self.pin_count = pin_count
        self.name = name

    def get_pin_count(self):
        return self.pin_count
