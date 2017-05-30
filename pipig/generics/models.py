from pipig.data import db, CRUDMixin


class GenericReading(db.Model, CRUDMixin):
    """
    Determines the output of a Sensor measurement
    """
    __tablename__ = "sensor_reading"
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
