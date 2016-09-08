from pipig.data import db, CRUDMixin


class Session(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)

    def __init__(self, name):
        self.name = name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

class CuringSession(db.Model, CRUDMixin):
    __tablename__ = 'session_curing'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    session_id = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Float)






