from pipig.data import db, CRUDMixin


class CuringSession(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    start_time = db.Column(db.Float, nullable=True)
    end_time = db.Column(db.Float, nullable=True)
    notes = db.Column(db.String, nullable=True)

    def __init__(self, name, start_time=None, notes=""):
        self.name = name
        self.start_time = start_time
        self.end_time = None
        self.notes = notes


    def __str__(self):
        return "Session\nID: " + str(self.get_id()) + "\nName: " + self.get_name() + "\nStart Time: " + str(self.get_start_time())

    def __eq__(self, other):
        equal_id = self.get_id() == other.get_id()
        equal_name = self.get_name() == other.get_name()
        equal_start_time = self.get_start_time() == other.get_start_time()
        return equal_id and equal_name and equal_start_time

    def get_json(self):
        json = {
            'id': self.get_id(),
            'name': self.get_name(),
            'start time': self.get_start_time(),
            'end time': self.get_end_time(),
            'notes': self.get_notes()
        }
        return json

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_notes(self):
        return self.notes

    def set_notes(self, updated_notes, append=False):
        """

        :param updated_notes: The new note to add
        :param append: Attaches the updated notes to the end of the existing notes
        :return: New notes
        """
        if append:
            self.notes = self.notes + "\n" + updated_notes
        else:
            self.notes = updated_notes
        return self.get_notes()

    def set_start_time(self, start_time):
        self.start_time = start_time

    def set_end_time(self, end_time):
        self.end_time = end_time

    def get_start_time(self):
        if self.start_time is None:
            return 0
        return self.start_time

    def get_end_time(self):
        if self.end_time is None:
            return 0
        return self.end_time

    def get_time_elapsed(self, reading_time):
        if reading_time < self.start_time:
            raise SessionTimeError
        return reading_time - self.start_time

    def get_reading_time(self, time_elapsed):
        return self.start_time + time_elapsed


class SessionTimeError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)






