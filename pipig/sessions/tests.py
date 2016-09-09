from test_helpers.test_base import BaseTestCase
from test_helpers.test_forms import FormTestCase
from test_helpers.test_generics import unwritten_test

from pipig import app
from sessions.models import Session, CuringSession



#________________________________________________________________
#
# Unit Tests
#________________________________________________________________

class SessionTests(BaseTestCase):
    def test_session(self):
        session = Session("Name")
        self.assertTrue(session.get_name() == "Name")


class CuringSessionTests(BaseTestCase):
    def compare_curing_session(self, first, second):
        session_id = first.session_id == second.session_id
        start_time = first.start_time == second.start_time
        return session_id and start_time

    def test_curing_session_commits_to_database_when_session_exists(self):

        with app.app_context():
            Session.create(name="TestSession")
            CuringSession.create(session_id=1, start_time=50.0)
            result = CuringSession.get(1)
        expected = CuringSession(1, 50.0)
        self.assertTrue(self.compare_curing_session(result, expected), "Curing sessions do not match \nResult: %s\nExpected: %s" % (result, expected))


    def test_curing_session_commits_to_database_when_session_doesnt_exist(self):
        CuringSession.create(session_id=2, start_time=50.0)
        with app.app_context():
            result = CuringSession.get(1)

        self.assertIsNone(result, "The curing session should not exist")

