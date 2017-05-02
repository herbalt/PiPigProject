from pipig.data import db, CRUDMixin


class Session(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    start_time = 0

    def __init__(self, name):
        self.name = name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def set_start_time(self, start_time):
        self.start_time = start_time

    def get_start_time(self):
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






