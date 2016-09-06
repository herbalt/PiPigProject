from pipig.data import db, CRUDMixin

class GpioPin(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    pin_number = db.Column(db.Integer, nullable=False)
    pin_name = db.Column(db.String)

