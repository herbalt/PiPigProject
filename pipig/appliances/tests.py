from appliances.models import Appliance, ApplianceType
from bindings_datapoints.datapoint_binding import IncorrectReadingTypeError
from generics.constants import COMPONENT_TYPE_DATAPOINTS_APPLIANCE_BINDER
from generics.models import GenericUnits,GenericReading
from appliances.appliance import BaseAppliance
from gpio_pins.models import GpioPin

from test_helpers.test_base import BaseTestCase
from test_helpers.test_generics import unwritten_test


from data import db


#________________________________________________________________
#
# Unit Tests
#________________________________________________________________

class ApplianceModelTests(BaseTestCase):
    def test_appliance(self):
        appliance_type = ApplianceType.create(type_name='TypeName', units_id=1)
        appliance = Appliance.create(name="Name", type_id=1)

        result = Appliance.get(appliance.get_id())

        self.assertTrue(result.get_name() == "Name", str(result))
        self.assertTrue(result.get_type_id() == 1, str(result))
        self.assertTrue(result.get_gpio_pin_id() is None, str(result))


class ApplianceObjectTests(BaseTestCase):

    def mock_base_appliance(self):
        return build_appliance_object("Test", "T", None)

    def mock_base_appliance_gpio(self):
        return build_appliance_object("Test", "T", 1)

    def test_get_id(self):
        test_obj = self.mock_base_appliance()
        self.assertTrue(test_obj.get_id() == 1, "ID is %d instead of 1" % test_obj.get_id())

    def test_get_name(self):
        test_obj = self.mock_base_appliance()
        self.assertTrue(test_obj.get_name() == "TestAppliance", "Name is %s instead of TestAppliance" % test_obj.get_name())

    def test_get_gpio_pin_id(self):
        test_obj = self.mock_base_appliance()
        test_obj_gpio = self.mock_base_appliance_gpio()
        self.assertIsNone(test_obj.get_gpio_pin_id(), "Gpio should be None")
        self.assertTrue(test_obj_gpio.get_gpio_pin_id() == 1, "Gpio is %d instead of 1" % test_obj_gpio.get_gpio_pin_id())

    def test_get_type(self):
        test_obj = self.mock_base_appliance()
        self.assertTrue(test_obj.get_type_id() == 1,
                        "Appliance Type ID is %d instead of 1" % test_obj.get_type_id())

    def test_get_units(self):
        test_obj = self.mock_base_appliance()
        self.assertTrue(test_obj.get_units() == "T",
                        "Appliance Units is %s instead of T" % test_obj.get_units())

    def test_get_state(self):
        test_obj = self.mock_base_appliance()
        self.assertIsNone(test_obj.get_state(), "State Inits incorrectly")

        test_obj.state = 1
        self.assertTrue(test_obj.get_state() == 1, "State correctly sets when accessed directly")

    def helper_test_receive(self, reading_value):
        obj = self.mock_base_appliance()
        input_reading = GenericReading(0, COMPONENT_TYPE_DATAPOINTS_APPLIANCE_BINDER, reading_value, 0)
        result = obj.receive(input_reading)
        self.assertTrue(obj.get_state() == reading_value)

    def test_receive(self):
        obj = self.mock_base_appliance()
        incorrect_reading_type = GenericReading(0, 0, 0, 0)
        self.assertRaises(IncorrectReadingTypeError, obj.receive, incorrect_reading_type)

        try:
            GenericReading(0, COMPONENT_TYPE_DATAPOINTS_APPLIANCE_BINDER, 0, 0)
        except IncorrectReadingTypeError:
            self.assertTrue(False, "Reading should not raise and error with the correct type id")


        self.helper_test_receive(1)
        self.helper_test_receive(0)

#________________________________________________________________
#
# Builders to use in Tests
#________________________________________________________________
def build_appliance_model(base_name, display_units, gpio_pin_number=None):
    units = GenericUnits.create(code_name="%sUnits" % base_name, display_units=display_units)
    type = ApplianceType.create(type_name="%sApplianceType" % base_name, units_id=units.get_id())

    if gpio_pin_number is not None:
        gpio_id = GpioPin.create(pin_number=gpio_pin_number, pin_name="%sPin%d" % (base_name, gpio_pin_number)).get_id()
    else:
        gpio_id = None
    appliance = Appliance.create(name="%sAppliance" % base_name, type_id=type.get_id(), gpio_pin_id=gpio_id)
    return appliance


def build_appliance_object(base_name, display_units, gpio_pin_number=None):
    appliance = build_appliance_model(base_name, display_units, gpio_pin_number)
    appliance_obj = TestObjectAppliance(appliance.get_id())
    return appliance_obj

class TestObjectAppliance(BaseAppliance):
    def process_result(self, result):
        return result