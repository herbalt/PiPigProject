from appliances.models import Appliance
from test_helpers.test_base import BaseTestCase
from test_helpers.test_forms import FormTestCase


#________________________________________________________________
#
# Unit Tests
#________________________________________________________________

class ApplianceTests(BaseTestCase):
    def test_appliance(self):
        appl = Appliance("Name")
        self.assertTrue(appl.get_name() == "Name")


