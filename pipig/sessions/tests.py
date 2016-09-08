from test_helpers.test_base import BaseTestCase
from test_helpers.test_forms import FormTestCase

from sessions.models import Session



#________________________________________________________________
#
# Unit Tests
#________________________________________________________________

class SessionTests(BaseTestCase):
    def test_session(self):
        session = Session("Name")
        self.assertTrue(session.get_name() == "Name")


