from pipig.data import db, CRUDMixin
from pipig import app

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

    def __init__(self, session_id, start_time):
        if self.validate_session_id(session_id):
            self.session_id = session_id
            self.start_time = start_time

    def __repr__(self):
        return "Curing Session ID: %s Session ID: %s StartTime: %s" % (str(self.id), str(self.session_id), str(self.start_time))

    def validate_session_id(self, session_id):
        with app.app_context():
            result = Session.get(session_id)

        if result is None:
            return False
        return True

    def get_session_id(self):
        return self.session_id

    def get_start_time(self):
        return self.start_time








