from curing_sessions.models import CuringSession, SessionTimeError
from test_helpers.test_base import BaseTestCase


#________________________________________________________________
#
# Unit Tests
#________________________________________________________________

class CuringSessionsModelTests(BaseTestCase):
    def test_session_name(self):
        curing_session = CuringSession.create(name="Name")
        self.assertTrue(curing_session.get_name() == "Name")

    def test_get_start_time(self):
        curing_session = CuringSession.create(name="Name")
        self.assertTrue(curing_session.get_start_time() == 0, "Session should init with a session time of 0")
        curing_session.start_time = 15.0
        self.assertTrue(curing_session.get_start_time() == 15.0, "Session should get a session time of 15.0 once the parameter is changed")

    def test_set_start_time(self):
        session = CuringSession.create(name="Name")
        session.set_start_time(10.0)
        self.assertTrue(session.get_start_time() == 10.0, "Session should be able to set a session time")

    def test_get_time_elapsed(self):
        session = CuringSession.create(name="Name")
        session.start_time = 15.0
        reading_time = 20.0
        result = session.get_time_elapsed(reading_time)
        self.assertTrue(result == 5.0, "Should be able to get a difference in start time and time elapsed values")

        reading_time = 10.0
        self.assertRaises(SessionTimeError, session.get_time_elapsed, reading_time)

    def test_get_reading_time(self):
        session = CuringSession.create(name="Name")
        session.start_time = 15.0
        time_elapsed = 10.0
        result = session.get_reading_time(time_elapsed)
        self.assertTrue(result == 25.0, "Should add together the start time and time elapsed values")

#________________________________________________________________
#
# Builders to use in Unit Tests
#________________________________________________________________

def build_curing_session_model(base_name):
    curing_session = CuringSession.create(name="%sSessionModel" % base_name)
    return curing_session


#________________________________________________________________
#
# Mock Object for Unit Tests
#________________________________________________________________
"""
class MockSession(Session):
    def __init__(self, name, self_id, start_time):
        super(MockSession, self).__init__(name)
        self.id = self_id
        self.start_time = start_time

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_start_time(self):
        return self.start_time
"""