from abc import abstractmethod, ABCMeta
from time import sleep

from general.patterns import Observer, Subject
from pipig import app

from sensors.sensors import Sensor, BasicSensor


class BaseProcessor(Observer, Subject):
    __metaclass__ = ABCMeta

    def __init__(self):
        Observer.__init__(self)
        Subject.__init__(self)
        # super(BaseProcessor, self).__init__()

    def receive(self, payload, status_code=0):
        result = self.process(payload, status_code)
        if result is not None:
            self.notify(result[0], result[1])
        return result

    @abstractmethod
    def process(self, payload, status_code=0):
        """
        :return: Payload after processing
        """


class ProcessorPrint(BaseProcessor):
    """
    Prints the payload to the Console
    """
    def process(self, payload, status_code=0):
        if payload is None:
            return None
        print "\nStatusCode: " + str(status_code) + \
              "\nPayload:" + str(payload)
        return payload, status_code


class ProcessorDelayQuantity(BaseProcessor):
    """
    Appends results to a list and returns the reading if list is full
    """
    def __init__(self, delay_quantity=1):
        super(ProcessorDelayQuantity, self).__init__()
        self.queue = []
        self.delay_quantity = delay_quantity

    def process(self, payload, status_code=0):
        self.queue.append((payload, status_code))
        if len(self.queue) >= self.delay_quantity:
            self.queue = []
            return payload, status_code
        return None

if __name__ == '__main__':
    sensor = BasicSensor(1)
    processor_print = ProcessorPrint()
    processor_delay = ProcessorDelayQuantity(100)

    processor_delay.attach(processor_print)
    sensor.attach(processor_delay)

    sensor.execute_operation(0.1)
    sleep(4)
    sensor.cancel_operation()
    sleep(0.5)