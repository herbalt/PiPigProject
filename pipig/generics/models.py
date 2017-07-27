from pipig.data import CRUDMixin, db


class GenericReading(db.Model, CRUDMixin):
    """
    Determines the output of a Sensor measurement
    """
    # TODO SHOULD ADD RECIPE IF KNOWN
    __tablename__ = "readings"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    component_id = db.Column(db.Integer)
    component_type_id = db.Column(db.Integer)
    reading_value = db.Column(db.Float)
    reading_timestamp = db.Column(db.Float)
    recipe_id = db.Column(db.Integer)
    type = db.Column(db.String(140))

    def __init__(self, component_id, component_type_id, reading_value, reading_timestamp, recipe_id=None):
        self.component_id = component_id
        self.component_type_id = component_type_id
        self.reading_value = reading_value
        self.reading_timestamp = reading_timestamp
        self.recipe_id = recipe_id

    def __str__(self):
        return "COMPONENT ID: " + str(self.component_id) + " TYPE ID: " + str(self.component_type_id) + " VALUE: " + str(self.reading_value) + " TIMESTAMP: " + str(self.reading_timestamp)

    def get_component_id(self):
        return self.component_id

    def get_component_type_id(self):
        return self.component_type_id

    def get_value(self):
        return self.reading_value

    def get_timestamp(self):
        return self.reading_timestamp

    def get_recipe_id(self):
        return self.recipe_id

    def get_json(self):
        reading_json = {
            'reading id': self.id,
            'component id': self.get_component_id(),
            'component type': self.get_component_type_id(),
            'value': self.get_value(),
            'timestamp': self.get_timestamp(),
            'recipe': self.get_recipe_id()
        }
        return reading_json


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

    def get_json(self):
        json = {
            'id': self.get_id(),
            'name': self.get_code_name(),
            'display': self.get_display_units()
        }
        return json