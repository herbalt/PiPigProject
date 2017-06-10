from abc import abstractmethod, ABCMeta

from appliances.models import Appliance, ApplianceType
# from pipig.bindings_datapoints.datapoint_binding import IncorrectReadingTypeError
from gpio_pins.models import GpioPin
from pipig.binders.models import IncorrectReadingTypeError
from general.patterns import Observer, Subject
from generics.constants import COMPONENT_TYPE_DATAPOINTS_APPLIANCE_BINDER
from generics.models import GenericUnits
from pipig import app

from gpio.config import GPIO


class BaseAppliance(Observer, Subject):
    __metaclass__ = ABCMeta

    def __init__(self, appliance_id):
        Observer.__init__(self)
        Subject.__init__(self)
        self.appliance_id = appliance_id
        self.state = None

    def get_id(self):
        return self.appliance_id

    def obj_appliance(self):
        obj = None
        with app.app_context():
            obj = Appliance.query.filter_by(id=self.get_id()).first()
            GPIO.setup(obj.get_gpio_pin(), GPIO.OUT)
        return obj

    def get_type(self):
        obj = ApplianceType.get(self.obj_appliance().get_type_id())
        return obj

    def obj_units(self):
        return GenericUnits.get(self.get_type().get_id())

    def get_name(self):
        return self.obj_appliance().get_name()

    def get_gpio_pin_id(self):
        return self.obj_appliance().get_gpio_pin_id()

    def get_gpio_pin(self):
        if self.obj_appliance().get_gpio_pin_id() is None:
            return None
        return GpioPin.get(self.obj_appliance().get_gpio_pin_id()).get_pin_number()

    def get_type_id(self):
        return self.obj_appliance().get_type_id()

    def get_units(self):
        return self.obj_units().get_display_units()


    def get_state(self):
        return self.state

    def receive(self, result, status_code=0):


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
        # print "%s is getting processed by the appliance %s" % (result, str(self))
        return result


class BasicAppliance(BaseAppliance):
    def process_result(self, result):
        print "\n%s is getting processed by the appliance %s" % (result, str(self))
        return result


class RelayAppliance(BaseAppliance):
    """
    Should turn on and off the relevant GPIO relay
    """
    def process_result(self, result):

        result.get_component_id()

        if result.get_value() > 0:
            GPIO.output(self.get_gpio_pin(), True)
        elif result.get_value() < 0:
            GPIO.output(self.get_gpio_pin(), False)
        return result

