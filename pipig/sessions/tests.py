from sessions.models import Session
from test_helpers.test_base import BaseTestCase
from test_helpers.test_forms import FormTestCase

class SessionTests(BaseTestCase):
    def test_appliance(self):
        appl = Session("Name")
        self.assertTrue(appl.get_name() == "Name")


