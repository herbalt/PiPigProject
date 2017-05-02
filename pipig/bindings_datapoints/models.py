from pipig.data import db, CRUDMixin


class BindDataPointsSensors(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    session_sensor_id = db.Column(db.Integer, nullable=False)
    datapoints_id = db.Column(db.Integer, nullable=False)

    def __init__(self, session_sensor_id, datapoints_id):
        self.session_sensor_id = session_sensor_id
        self.datapoints_id = datapoints_id

    def get_id(self):
        return self.id

    def get_session_sensor_id(self):
        return self.session_sensor_id

    def get_datapoints_id(self):
        return self.datapoints_id


class BindDataPointsAppliances(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    session_appliance_id = db.Column(db.Integer, nullable=False)
    datapoints_id = db.Column(db.Integer, nullable=False)
    polarity = db.Column(db.Integer, default=1)

    def __init__(self, session_appliance_id, datapoints_id, polarity=1):
        self.session_appliance_id = session_appliance_id
        self.datapoints_id = datapoints_id
        self.polarity = polarity

    def get_id(self):
        return self.id

    def get_session_appliance_id(self):
        return self.session_appliance_id

    def get_datapoints_id(self):
        return self.datapoints_id

    def get_polarity(self):
        return self.polarity





