from pi_gpio import config
from abc import abstractmethod, ABCMeta
from pipig.data import db, CRUDMixin


class GpioPin(db.Model, CRUDMixin):
    __tablename__ = "gpio_pin"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    pin_position = db.Column(db.Integer, nullable=False)
    pin_number = db.Column(db.Integer, nullable=True)
    pin_name = db.Column(db.String)
    bcm_pin = db.Column(db.Integer, nullable=True)

    def __init__(self, pin_position, pin_number, bcm_pin, pin_name=""):
        self.pin_position = pin_position
        self.pin_number = pin_number
        self.bcm_pin = bcm_pin
        self.pin_name = pin_name

    def get_id(self):
        return self.id

    def get_pin_number(self):
        if config.GPIO.getmode() == "BCM":
            return self.bcm_pin
        else:
            return self.pin_number

    def get_pin_name(self):
        return self.pin_name


class RaspberryPi(db.Model, CRUDMixin):
    __metaclass__ = ABCMeta

    __tablename__ = "raspberry_pi"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    pin_count = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String)

    def __init__(self, pin_count, name):
        self.pin_count = pin_count
        self.name = name

    def get_pin_count(self):
        return self.pin_count

