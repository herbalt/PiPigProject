from pipig.data import db

class SensorType(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    sensor_type = db.Column(db.String(140))

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String)
    sensor_factory_id = db.Column(db.Integer)
    interval_between_readings = db.Column(db.Float)
    state = db.Column(db.Boolean, default=False)

    def __init__(self, name, sensor_factory_id, interval_between_readings):
        self.name = name
        self.sensor_factory_id = sensor_factory_id
        self.interval_between_readings = interval_between_readings

    def __str__(self):
        return "Id: " + str(self.id) + \
               " Name:" + self.name + \
               " FactoryId: " + str(self.interval_between_readings) + \
               " Interval: " + str(self.interval_between_readings) + \
               " State: " + str(self.state)


class SensorReading(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    sensor_id = db.Column(db.Integer)
    reading_value = db.Column(db.Float)
    reading_timestamp = db.Column(db.DateTime)


