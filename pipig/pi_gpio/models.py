from pi_gpio import config
from pipig.data import db, CRUDMixin
from pi_gpio.GPIO_Placeholder import BCM, BOARD, HIGH, IN, LOW, OUT
from pi_gpio.config import GPIO

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

    def get_json(self):
        json = {
            'pin number': self.get_pin_number(),
            'pin name': self.get_pin_name(),
            'pin position': self.get_pin_position()
        }
        return json
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

    def get_pin_position(self):
        return self.pin_position

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

    def get_id(self):
        return self.id

    def get_pin_count(self):
        return self.pin_count

    def get_model(self):
        return self.name

    def get_json(self):
        pin_list = []
        for i in range(1, self.pin_count + 1):
            pin = GpioPin.get(i)
            pin_list.append(pin.get_json())

        pi_json = {
            'id': self.id,
            'model': self.get_model(),
            'pi pins': pin_list
        }

        return pi_json

    def configure_application(self, input_pin_list=None, output_pin_list=None):
        """

        :param input_pin_list: List of Pin Positions that will require configuration for GPIO Input
        :param output_pin_list: List of Pin Positions that will require configuration for GPIO Output
        :return:
        """
        for input_pin in input_pin_list:
            if input_pin is not None:
                GPIO.setup(input_pin, GPIO.IN)

        for output_pin in output_pin_list:
            if output_pin is not None:
                GPIO.setup(output_pin, GPIO.OUT)
