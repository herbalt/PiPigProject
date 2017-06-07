from abc import abstractmethod, ABCMeta
from time import sleep
import inspect
from pipig.utilities import debug_messenger
from general.patterns import Observer, Subject
from sensors.sensor import SensorBasic
from generics.models import GenericReading
from utilities import average_readings, calculate_quantity_of_readings
from pipig.data import db, CRUDMixin
from sensors.factory import FactorySensor
from pipig import app

class BaseProcessor(Observer, Subject):
    """
    Template Pattern for processing a Sensor Reading

    Attach the Processor to a sensor or another Processor
    Notify all attached observers of the Processed message
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        Observer.__init__(self)
        Subject.__init__(self)

    def receive(self, payload, status_code=0):
        """
        Method that is called when a Subject notifys its observers
        :param payload:
        :param status_code:
        :return:
        """

        result = self.process(payload, status_code)
        if result is not None:
            self.notify(result, status_code)
        return result

    @abstractmethod
    def process(self, payload, status_code=0):
        """
        Method to over-ride with the specific type_name of processing to apply
        :return: Payload after processing
        """


class ProcessorPrint(BaseProcessor):
    """
    Prints the payload to the Console
    """
    def process(self, payload, status_code=0):
        """

        :param payload: A sensor reading payload
        :param status_code: The status code from the Async Task
        :return: A sensor reading payload
        """
        if payload is None:
            return None
        print "\nStatusCode: " + str(status_code) + \
              "\nPayload:" + str(payload)
        return payload


class ProcessorAverageDelay(BaseProcessor):
    """
    Appends results to a list and returns the reading if list is full
    If average is True: Average the values of the list and use the last timestamp
    """
    def __init__(self, delay_quantity=1, average=False):
        super(ProcessorAverageDelay, self).__init__()
        self.queue = []
        self.delay_quantity = delay_quantity
        self.average = average

    def update_delay_quantity_by_time(self, delay_in_seconds=1, interval_between_readings=1):
        self.delay_quantity = calculate_quantity_of_readings(timeframe_in_seconds=delay_in_seconds,
                                       interval_between_readings=interval_between_readings)

    def update_delay_quantity(self, delay_quantity=1):
        self.delay_quantity = delay_quantity

    def process(self, payload, status_code=0):
        self.queue.append((payload, status_code))
        if len(self.queue) >= self.delay_quantity:
            if self.average:
                value_list = []
                for reading in self.queue:
                    value_list.append(reading[0].get_value())
                average_value = average_readings(value_list)

                return_reading = GenericReading(payload.get_component_id(), payload.get_component_type_id(), average_value, payload.get_timestamp())
            else:
                return_reading = payload
            self.queue = []
            return return_reading
        return None


class ProcessorDatabase(BaseProcessor):
    def __init__(self):
        super(ProcessorDatabase, self).__init__()

    def process(self, payload, status_code=0):
        debug_messenger("READING TO DATABASE:\n" + str(payload))
        gti= payload.get_component_id()
        gcti = payload.get_component_type_id()
        gv = payload.get_value()
        gt = payload.get_timestamp()
        # GenericReading(component_id=1, component_type_id=1, reading_value=1, reading_timestamp=1)
        with app.app_context():
            result = GenericReading.create(component_id=payload.get_component_id(),
                                  component_type_id=payload.get_component_type_id(),
                                  reading_value=payload.get_value(),
                                  reading_timestamp=payload.get_timestamp())
        return result


def build_processor_chain(delay_quantity=1, average=False):
    processor_print = ProcessorPrint()
    processor_database = ProcessorDatabase()
    processor_delay = ProcessorAverageDelay(delay_quantity=delay_quantity, average=average)

    processor_delay.attach(processor_print)
    processor_delay.attach(processor_database)

    return processor_delay

if __name__ == '__main__':
    sensor = SensorBasic(1)
    # sensor_factory = FactorySensor()
    # sensor = sensor_factory.build_object(1)
    processor_print = ProcessorPrint()
    # processor_print = ProcessorDatabase()
    interval = sensor.get_interval_between_readings()
    delay_count = calculate_quantity_of_readings(timeframe_in_seconds=100, interval_between_readings=interval)
    processor_delay = ProcessorAverageDelay(delay_count)

    processor_delay.attach(processor_print)
    sensor.attach(processor_delay)

    sensor.execute_operation(0.1)
    sleep(4)
    sensor.cancel_operation()
    sleep(0.5)