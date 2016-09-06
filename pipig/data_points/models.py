from pipig.data import db, CRUDMixin

class DataPoint(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    session_id = db.Column(db.Integer, nullable=False)
    data_point_value = db.Column(db.Float)
    data_point_time = db.Column(db.Float)

