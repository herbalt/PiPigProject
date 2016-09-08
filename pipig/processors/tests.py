from test_helpers.test_base import BaseTestCase
from test_helpers.test_forms import FormTestCase

from test_helpers.test_generics import unwritten_test
from processors import  ProcessorAverageDelay, BaseSensorReadingProcessor
from sensors.models import SensorReadings
from general.patterns import Observer, Subject
#________________________________________________________________
#
# Unit Tests
#________________________________________________________________

class ProcessorsTests(BaseTestCase):

    def test_base_sensor_template(self):
        processor = ObjectBaseSensorReadingProcessor()
        reading = SensorReadings(1, 2, 3.0)
        result = processor.receive(reading, 4)
        self.assertTrue(isinstance(result, SensorReadings), "Return result should be a Sensor Reading Object: " + str(result))

    def test_average_delay(self):
        average_processor = ProcessorAverageDelay(delay_quantity=3)
        queue = ObjectObserver()
        sensor = ObjectMockSensorSubject()

        average_processor.attach(queue)
        sensor.attach(average_processor)

        sensor.trigger(loop_times=4)


        unwritten_test(self)

    def test_average_delay_no_average(self):
        unwritten_test(self)

    def test_database_commits_reading(self):
        unwritten_test(self)


#________________________________________________________________
#
# Objects for Unit Tests
#________________________________________________________________


class ObjectBaseSensorReadingProcessor(BaseSensorReadingProcessor):
    def process(self, payload, status_code=0):
        return payload


class ObjectObserver(Observer):

    def __init__(self):
        Observer.__init__(self)
        self.queue = []


    def receive(self, result, status_code=0):
        self.queue.append((result, status_code))

    def get_queue(self):
        return self.queue

    def clear_queue(self):
        self.queue = []

class ObjectMockSensorSubject(Subject):
    def __init__(self):
        super(ObjectMockSensorSubject, self).__init__()
        self.counter = 0
        self.timer = 100.0

    def trigger(self, loop_times=1, number_to_increment=1, timer_to_increment=100):
        while loop_times > 0:
            self.counter += number_to_increment
            self.timer += timer_to_increment
            result = SensorReadings(1, self.counter, self.timer)
            self.notify(result, 2)
            loop_times -= 1


