from abc import abstractmethod, ABCMeta

from appliances.models import Appliance, ApplianceType
from bindings_datapoints.datapoint_binding import IncorrectReadingTypeError
from general.patterns import Observer, Subject
from generics.constants import COMPONENT_TYPE_DATAPOINTS_APPLIANCE_BINDER
from units.models import GenericUnits
from pipig import app


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
        return obj

    def obj_type(self):
        obj = ApplianceType.get(self.obj_appliance().get_type_id())
        return obj

    def obj_units(self):
        return GenericUnits.get(self.obj_type().get_id())

    def get_name(self):
        return self.obj_appliance().get_name()

    def get_gpio_pin_id(self):
        return self.obj_appliance().get_gpio_pin_id()

    def get_type_id(self):
        return self.obj_appliance().get_type_id()

    def get_units(self):
        return self.obj_units().get_display_units()


    def get_state(self):
        return self.state

    def receive(self, result, status_code=0):

        if result.get_component_type_id() != COMPONENT_TYPE_DATAPOINTS_APPLIANCE_BINDER:
            raise IncorrectReadingTypeError

        result = self.process_result(result)
        self.state = result.get_value()

    @abstractmethod
    def process_result(self, result):
        """
        Over ride this method for different implementations. Example GPIO Relay, Debug Printer.
        This is an implementation of a Debug Printer
        :param result:
        :return:
        """
        print "%s is getting processed by the appliance %s" % (result, str(self))
        return result


class BasicAppliance(BaseAppliance):
    def process_result(self, result):
        print "%s is getting processed by the appliance %s" % (result, str(self))
        return result