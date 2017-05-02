from data import CRUDMixin
from pipig import db

class BindSessionsSensors(db.Model, CRUDMixin):
    """
    Binds a Sensor to a Session
    """
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    session_id = db.Column(db.Integer, nullable=False)
    sensor_id = db.Column(db.Integer, nullable=False)

    def __init__(self, session_id, sensor_id):
        self.session_id = session_id
        self.sensor_id = sensor_id

    def get_id(self):
        return self.id

    def get_session_id(self):
        return self.session_id

    def get_sensor_id(self):
        return self.sensor_id


class BindSessionAppliances(db.Model, CRUDMixin):
    """
    Binds an Appliance to a Session
    """
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    session_id = db.Column(db.Integer, nullable=False)
    appliance_id = db.Column(db.Integer, nullable=False)

    def __init__(self, session_id, appliance_id):
        self.session_id = session_id
        self.appliance_id = appliance_id

    def get_id(self):
        return self.id

    def get_session_id(self):
        return self.session_id

    def get_appliance_id(self):
        return self.appliance_id


