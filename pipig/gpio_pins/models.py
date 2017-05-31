from pipig.data import db, CRUDMixin

class GpioPin(db.Model, CRUDMixin):
    __tablename__ = "gpio_pin"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    pin_number = db.Column(db.Integer, nullable=False)
    pin_name = db.Column(db.String)

    def __init__(self, pin_number, pin_name):
        self.pin_number = pin_number
        self.pin_name = pin_name

    def get_id(self):
        return self.id

    def get_pin_number(self):
        return self.pin_number

    def get_pin_name(self):
        return self.pin_name

