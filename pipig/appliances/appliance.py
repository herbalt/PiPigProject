from abc import abstractmethod, ABCMeta
from pipig import app
from appliances.models import Appliance, ApplianceType
from gpio_pins.models import GpioPin
from general.patterns import Observer, Subject
from generics.constants import COMPONENT_TYPE_DATAPOINTS_APPLIANCE_BINDER
from generics.models import GenericUnits
from gpio.config import GPIO


class BaseAppliance(Observer, Subject):
    # TODO Requires a way to  setup the GPIO Pin Setup to GPIO.OUT
    __metaclass__ = ABCMeta

    gpio_pin = None

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
        return self.obj_appliance().get_name()

    def get_gpio_pin_id(self):
        return self.obj_appliance().get_gpio_pin_id()

    def get_gpio_pin(self):
        if self.gpio_pin is not None:
            return self.gpio_pin.get_pin_number()
        if self.obj_appliance().get_gpio_pin_id() is None:
            return None

        pin = None
        with app.app_context():
            pin = GpioPin.get(self.obj_appliance().get_gpio_pin_id()).get_pin_number()
        return pin

    def get_type_id(self):
        return self.obj_appliance().get_type_id()

    def get_units(self):
        return self.obj_units().get_display_units()

    def get_state(self):
        return self.state

    """
    OBJECT METHODS
    """
    def obj_appliance(self):
        with app.app_context():
            appliance = Appliance.get(id=self.get_id())
        return appliance

    def obj_type(self):
        return ApplianceType.get(self.obj_appliance().get_type_id())

    def obj_units(self):
        return GenericUnits.get(self.obj_type().get_id())

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
        print "\n%s is getting processed by the appliance %s" % (result, str(self))
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

