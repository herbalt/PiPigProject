from pipig.data import db, CRUDMixin


class SensorType(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    sensor_type = db.Column(db.String(140))
    sensor_units_id = db.Column(db.Integer)
    minimum_refresh = db.Column(db.Float(), default=0)

    def __init__(self, sensor_type, sensor_units_id=0, minimum_refresh=0.0):
        self.sensor_type = sensor_type
        self.sensor_units_id = sensor_units_id
        self.minimum_refresh = minimum_refresh

    def get_id(self):
        return self.id

    def get_sensor_type(self):
        return self.sensor_type

    def get_sensor_units_id(self):
        return self.sensor_units_id

    def get_minimum_refresh(self):
        return self.minimum_refresh

class SensorUnits(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key= True, nullable=False)
    code_name = db.Column(db.String, nullable=False)
    display_units = db.Column(db.String(4), nullable=True)

    def __init__(self, code_name, display_units):
        self.code_name = code_name
        self.display_units = display_units

    def get_code_name(self):
        return self.code_name

    def get_display_units(self):
        return self.display_units


class Sensor(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String)
    sensor_type_id = db.Column(db.Integer)
    interval_between_readings = db.Column(db.Float)
    state = db.Column(db.Boolean, default=False)

    def __init__(self, name, sensor_type_id, interval_between_readings):
        self.name = name
        self.sensor_type_id = sensor_type_id
        self.interval_between_readings = interval_between_readings

    def __str__(self):
        return "Id: " + str(self.id) + \
               " Name:" + self.name + \
               " SensorTypeId: " + str(self.sensor_type_id) + \
               " Interval: " + str(self.interval_between_readings) + \
               " State: " + str(self.state)

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_sensor_type_id(self):
        return self.sensor_type_id

    def get_interval_between_readings(self):
        return self.interval_between_readings


class SensorReadings(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    sensor_id = db.Column(db.Integer)
    reading_value = db.Column(db.Float)
    reading_timestamp = db.Column(db.Float)

    def __init__(self, sensor_id, reading_value, reading_timestamp):
        self.sensor_id = sensor_id
        self.reading_value = reading_value
        self.reading_timestamp = reading_timestamp
