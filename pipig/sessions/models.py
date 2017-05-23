from pipig.data import db, CRUDMixin


class Session(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)

    def __init__(self, name, start_time=None):
        self.name = name
        self.start_time = start_time

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def set_start_time(self, start_time):
        self.start_time = start_time

    def get_start_time(self):
        if self.start_time is None:
            return 0
        return self.start_time

    def get_time_elapsed(self, reading_time):
        if reading_time < self.start_time:
            raise SessionTimeError
        return reading_time - self.start_time

    def get_reading_time(self, time_elapsed):
        return self.start_time + time_elapsed


class SessionTimeError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)






