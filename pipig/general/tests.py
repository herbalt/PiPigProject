from test_helpers.test_base import BaseTestCase
from pipig.general.patterns import AsyncTask, Observer
from time import sleep, time


class TestAsyncTask(AsyncTask):
    counter = None

    def pre_execute(self, payload=None):
        self.counter = 0
        return self.counter

    def operation(self, params=None):
        for i in range(0, 5):
            if self.is_cancelled():
                return self.counter, AsyncTask.STATUS_CODE_CANCEL
            self.counter += 1
            self.on_progress(self.counter)
            sleep(params)
        return self.counter


class ObjectObserver(Observer):
    results = []

    def update(self, payload, status_code=0):
        self.results.append((status_code, payload))

    def get_results(self):
        return self.results

    def clear(self):
        self.results = []

class AsyncTaskTests(BaseTestCase):
    def test_operation_complete(self):
        task = TestAsyncTask()
        observe = ObjectObserver()
        observe.clear()
        task.attach(observe)
        task.execute_operation(0.01)
        sleep(0.08)
        results = observe.get_results()
        expected_list = [(1, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (3, 5)]

        results_first_status = results[0][0]
        results_middle_status = results[1][0]
        results_last_status = results[-1][0]

        self.assertIs(results_first_status, 1, "Pre Execute Status Code Incorrect %s" % str(results))
        self.assertIs(results_middle_status, 2, "Progress Status Code Incorrect %s" % str(results))
        self.assertIs(results_last_status, 3, "Complete Status Code Incorrect %s" % str(results))

        results_first_payload = results[0][1]
        results_middle_payload = results[1][1]
        results_last_payload = results[-1][1]

        self.assertTrue(type(results_first_payload) == type(1), "Pre Execute Payload Incorrect %s" % str(results))
        self.assertTrue(type(results_middle_payload) == type(1), "Progress Payload Incorrect %s" % str(results))
        self.assertTrue(type(results_last_payload) == type(1), "Complete Payload Incorrect %s" % str(results))


    def test_operation_cancel(self):
        task = TestAsyncTask()
        observe = ObjectObserver()
        observe.clear()
        task.attach(observe)
        task.execute_operation(0.01)
        sleep(0.03)
        task.cancel_operation()
        sleep(0.02)
        results = observe.get_results()
        expected_list = [(1, 0), (2, 1), (2, 2), (2, 3), (2, 4), (4, 4)]

        results_first_status = results[0][0]
        results_middle_status = results[1][0]
        results_last_status = results[-1][0]

        self.assertIs(results_first_status, 1, "Pre Execute Status Code Incorrect %s" % str(results))
        self.assertIs(results_middle_status, 2, "Progress Status Code Incorrect %s" % str(results))
        self.assertIs(results_last_status, 4, "Cancel Status Code Incorrect %s" % str(results))

        results_last_payload = results[-1][1]

        self.assertTrue(type(results_last_payload) == type(1), "Cancel Payload Incorrect")
