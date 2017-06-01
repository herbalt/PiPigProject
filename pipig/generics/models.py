from pipig.data import CRUDMixin, db


class GenericReading(db.Model, CRUDMixin):
    """
    Determines the output of a Sensor measurement
    """
    __tablename__ = "readings"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    component_id = db.Column(db.Integer)
    component_type_id = db.Column(db.Integer)
    reading_value = db.Column(db.Float)
    reading_timestamp = db.Column(db.Float)
    type = db.Column(db.String(140))

    def __init__(self, component_id, component_type_id, reading_value, reading_timestamp):
        self.component_id = component_id
        self.component_type_id = component_type_id
        self.reading_value = reading_value
        self.reading_timestamp = reading_timestamp

    def __str__(self):
        return "Component ID: " + str(self.component_id) + "\nComponent Type ID: " + str(self.component_type_id) + "\nValue: " + str(self.reading_value) + "\nTimestamp: " + str(self.reading_timestamp)

    def get_component_id(self):
        return self.component_id

    def get_component_type_id(self):
        return self.component_type_id

    def get_value(self):
        return self.reading_value

    def get_timestamp(self):
        return self.reading_timestamp


class GenericUnits(db.Model, CRUDMixin):
    """
    Determines the Units of measures
    Example Celcius, Humidty, TestInteger
    """
    __tablename__ = "units"
    id = db.Column(db.Integer, primary_key= True, nullable=False)
    code_name = db.Column(db.String, nullable=False)
    display_units = db.Column(db.String(4), nullable=True)

    # TODO WHY IS TYPE HERE ?
    type = db.Column(db.String(140))

    def __init__(self, code_name, display_units):
        self.code_name = code_name
        self.display_units = display_units

    def get_id(self):
        return self.id

    def get_code_name(self):
        return self.code_name

    def get_display_units(self):
        return self.display_units