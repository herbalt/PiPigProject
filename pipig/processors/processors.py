from abc import abstractmethod, ABCMeta
from time import sleep
import inspect

from general.patterns import Observer, Subject
from sensors.sensors import SensorReadings, BasicSensor
from utilities import average_readings, calculate_quantity_of_readings
from pipig.data import db, CRUDMixin


class BaseSensorReadingProcessor(Observer, Subject):
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
        Method to over-ride with the specific type of processing to apply
        :return: Payload after processing
        """


class ProcessorPrint(BaseSensorReadingProcessor):
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


class ProcessorAverageDelay(BaseSensorReadingProcessor):
    """
    Appends results to a list and returns the reading if list is full
    If average is True: Average the values of the list and use the last timestamp
    """
    def __init__(self, delay_quantity=1, average=False):
        super(ProcessorAverageDelay, self).__init__()
        self.queue = []
        self.delay_quantity = delay_quantity
        self.average = average

    def process(self, payload, status_code=0):
        self.queue.append((payload, status_code))
        if len(self.queue) >= self.delay_quantity:
            if self.average:
                value_list = []
                for reading in self.queue:
                    value_list.append(reading[0].get_value())
                average_value = average_readings(value_list)

                return_reading = SensorReadings(payload.get_sensor_id(), average_value, payload.get_timestamp())
            else:
                return_reading = payload
            self.queue = []
            return return_reading
        return None


class ProcessorDatabase(BaseSensorReadingProcessor):
    def __init__(self):
        super(ProcessorDatabase, self).__init__()

    def process(self, payload, status_code=0):
        db.session.add(payload)
        db.session.commit()
        return payload




if __name__ == '__main__':
    sensor = BasicSensor(1)
    processor_print = ProcessorPrint()
    delay_count = calculate_quantity_of_readings(100, sensor.get_interval_between_readings())
    processor_delay = ProcessorAverageDelay(delay_count)

    processor_delay.attach(processor_print)
    sensor.attach(processor_delay)

    sensor.execute_operation(0.1)
    sleep(4)
    sensor.cancel_operation()
    sleep(0.5)