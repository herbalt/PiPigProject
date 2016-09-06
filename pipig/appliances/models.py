from pipig.data import db, CRUDMixin


class Appliance(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)

    def __init__(self, name):
        self.name = name