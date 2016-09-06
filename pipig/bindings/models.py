from pipig.data import db, CRUDMixin


class BindSessionAppliances(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    session_id = db.Column(db.Integer, nullable=False)
    appliance_id = db.Column(db.Integer, nullable=False)
    gpio_pin_id = db.Column(db.Integer, nullable=True)


class BindSessionsSensors(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    session_id = db.Column(db.Integer, nullable=False)
    sensor_id = db.Column(db.Integer, nullable=False)
    gpio_pin_id = db.Column(db.Integer, nullable=True)


class BindDataPointsAppliances(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data_point_id = db.Column(db.Integer, nullable=False)
    appliance_id = db.Column(db.Integer, nullable=False)
    polarity = db.Column(db.Boolean)


class BindDataPointsSensors(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data_point_id = db.Column(db.Integer, nullable=False)
    sensor_id = db.Column(db.Integer, nullable=False)




