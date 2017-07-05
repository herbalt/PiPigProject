from test_helpers.test_base import BaseTestCase
from test_helpers.test_forms import FormTestCase

from test_helpers.test_generics import unwritten_test
from processors import ProcessorAverageDelay, BaseProcessor
from generics.models import GenericReading
from general.patterns import Observer, Subject
from pipig import app
from pipig.data import db, CRUDMixin
#________________________________________________________________
#
# Unit Tests
#________________________________________________________________


class ProcessorObjectTests(BaseTestCase):

    def test_base_sensor_template(self):
        processor = ObjectBaseProcessor()
        reading = GenericReading(1, 1, 2, 3.0)
        result = processor.receive(reading, 4)
        self.assertTrue(isinstance(result, GenericReading), "Return result should be a Sensor Reading Object: " + str(result))

    def helper_delay_processor(self, expected=None, loop_times=1, average=False):
        average_processor = ProcessorAverageDelay(delay_quantity=3, average=average)
        queue = ObjectObserver()
        sensor = ObjectMockSensorSubject()

        average_processor.attach(queue)
        sensor.attach(average_processor)

        sensor.trigger(loop_times=loop_times)

        result = queue.get_queue()

        self.assertTrue(self.compare_readings_list(result, expected))


    def compare_readings_list(self, first, second):
        if len(first) == len(second):
            for index in range(0, len(first) - 1):
                if not self.compare_sensor_readings(first[index][0], second[index][0]):
                    return False
            return True
        return False

    def compare_sensor_readings(self, first, second):
        id = first.get_component_id() == second.get_component_id()
        value = first.get_value() == second.get_value()
        timestamp = first.get_timestamp() == second.get_timestamp()
        return id and value and timestamp


    def test_average_delay(self):
        expected = []
        expected.append((GenericReading(1, 1, 2, 400), 2))
        expected.append((GenericReading(1, 1, 5, 700), 2))
        expected.append((GenericReading(1, 1, 8, 1000), 2))
        self.helper_delay_processor(expected, 9, True)


    def test_average_delay_no_average(self):
        expected = []
        expected.append((GenericReading(1, 1, 3, 400), 2))
        expected.append((GenericReading(1, 1, 6, 700), 2))
        expected.append((GenericReading(1, 1, 9, 1000), 2))
        self.helper_delay_processor(expected, 9, False)

    # TODO This test should be moved to test if the Controller can process to the database
    """
    def test_database_commits_reading(self):
        database_processor = ProcessorDatabase()
        serial_sensor = ObjectMockSensorSubject()
        queue = ObjectObserver()

        database_processor.attach(queue)
        serial_sensor.attach(database_processor)

        serial_sensor.trigger(loop_times=2)

        with app.app_context():
            reading = GenericReading.get(1)
        self.assertIsNotNone(reading)
        self.assertTrue(self.compare_sensor_readings(GenericReading(1, 1, 1, 200), reading))
    """



#________________________________________________________________
#
# Objects for Unit Tests
#________________________________________________________________

class ObjectBaseProcessor(BaseProcessor):
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
            result = GenericReading(1, 1, self.counter, self.timer)
            self.notify(result, 2)
            loop_times -= 1
