from abc import abstractmethod, ABCMeta

from appliances.models import Appliance, ApplianceType
from general.patterns import Observer, Subject
from generics.constants import COMPONENT_TYPE_DATAPOINTS_APPLIANCE_BINDER
from generics.models import GenericUnits
from pi_gpio.config import GPIO
from pi_gpio.models import GpioPin
from pipig import app
from utilities import debug_messenger


class BaseAppliance(Observer, Subject):
    # TODO Requires a way to  setup the GPIO Pin Setup to GPIO.OUT
    __metaclass__ = ABCMeta

    gpio_pin = None
    appliance_model = None
    type_model = None
    units_model = None

    def __init__(self, appliance_id):
        Observer.__init__(self)
        Subject.__init__(self)
        self.appliance_id = appliance_id
        self.state = None

    def __str__(self):
        return "APPLIANCE ID: " + str(self.appliance_id()) + " STATE: " + str(self.get_state())

    """
    GET METHODS
    """
    def get_id(self):
        return self.appliance_id

    def get_name(self):
        return self.obj_appliance_model().get_name()

    def get_gpio_pin_id(self):
        return self.obj_appliance_model().get_gpio_pin_id()

    def get_gpio_pin(self):
        if self.gpio_pin is not None:
            return self.gpio_pin.get_pin_number()
        if self.get_gpio_pin_id() is None:
            debug_messenger("Appliance GPIO does not exist in Database")
            return None
        with app.app_context():
            self.gpio_pin = GpioPin.get(self.get_gpio_pin_id())
        return self.gpio_pin.get_pin_number()

    def get_type_id(self):
        return self.obj_appliance_model().get_type_id()

    def get_units(self):
        return self.obj_units().get_display_units()

    def get_state(self):
        return self.state

    """
    OBJECT METHODS
    """
    def obj_appliance_model(self):
        if self.appliance_model is None:
            # with app.app_context():
            self.appliance_model = Appliance.get(id=self.get_id())
            if self.appliance_model is None:
                raise IndexError

        return self.appliance_model

    def obj_type(self):
        if self.type_model is None:
            self.type_model = ApplianceType.get(self.obj_appliance_model().get_type_id())
        return self.type_model

    def obj_units(self):
        if self.units_model is None:
            self.units_model = GenericUnits.get(self.obj_type().get_id())
        return self.units_model

    """
    OVER RIDE METHODS
    """
    def receive(self, result, status_code=0):
        """
        Template Pattern Method to process a result from a Subject
        :param result: Reading that is from a Datapoints Appliance Binder
        :param status_code:
        :return:
        """
        if result.get_component_type_id() == COMPONENT_TYPE_DATAPOINTS_APPLIANCE_BINDER:
            result = self.process_result(result)
            self.state = result.get_value()
        else:
            raise AttributeError

    @abstractmethod
    def process_result(self, result):
        """
        Over ride this method for different implementations. Example GPIO Relay, Debug Printer.
        This is an implementation of a Debug Printer
        :param result:
        :return:
        """
        return result


class BasicAppliance(BaseAppliance):
    """
    The Generic Appliance that only returns the result
    """
    def process_result(self, result):
        return result


class PrintAppliance(BaseAppliance):
    """
    The Generic Appliance that prints the result
    """
    def process_result(self, result):
        print "\n%s is getting processed by the appliance_model %s" % (result, str(self))
        return result


class RelayAppliance(BaseAppliance):
    """
    Should turn on and off the relevant GPIO relay
    """

    def process_result(self, result):

        result.get_component_id()
        value = result.get_value()
        if value > 0:
            GPIO.output(self.get_gpio_pin(), GPIO.HIGH)
        elif value < 0:
            GPIO.output(self.get_gpio_pin(), GPIO.LOW)
        return result

