from pipig.data import db, CRUDMixin


class ApplianceType(db.Model, CRUDMixin):
    __tablename__ = 'appliance_type'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    type_name = db.Column(db.String, nullable=False)
    units_id = db.Column(db.Integer, nullable=False)

    def __init__(self, type_name, units_id):
        self.type_name = type_name
        self.units_id = units_id

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type_name

    def get_units_id(self):
        return self.units_id


class Appliance(db.Model, CRUDMixin):
    __tablename__ = 'appliance_model'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    type_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    gpio_pin_id = db.Column(db.Integer, nullable=True, default=None)


    def __init__(self, name, type_id, gpio_pin_id=None):
        self.name = name
        self.type_id = type_id
        self.gpio_pin_id = gpio_pin_id

    def __str__(self):
        return "Appliance\nName: " + self.name + "\nType ID: " + str(self.type_id) + "\nGPIO Pin: " + str(self.gpio_pin_id)

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_type_id(self):
        return self.type_id

    def get_gpio_pin_id(self):
        return self.gpio_pin_id




