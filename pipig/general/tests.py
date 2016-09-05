from test_helpers.test_base import BaseTestCase
from pipig.general.patterns import AsyncTask, Observer
from time import sleep


class SubjectTests(BaseTestCase):

    def test_attach(self):
        self.assertTrue(False, "Not implemented")

    def test_detach(self):
        self.assertTrue(False, "Not implemented")

    def test_notify(self):
        self.assertTrue(False, "Not implemented")


class AsyncThreadTests(BaseTestCase):

    def test_run(self):
        self.assertTrue(False, "Not implemented")

class MockAsyncTask(AsyncTask):
    def __init__(self):
        super(MockAsyncTask, self).__init__()
        self.counter = None
        self.interval = 0.002

    def pre_execute(self, payload=None):
        self.counter = 0

    def operation(self, params):
        for i in range(0, 10):
            if self.is_cancelled():
                return self.on_cancel(None)
            self.counter += 1
            self.on_progress(self.counter)
            sleep(self.interval)
        return self.counter

    def post_execute(self, result):
        return ("POST EXECUTE", result)

    def progress(self, payload):
        return (payload)

    def cancel(self, result):
        return ("CANCELLED", result)


class AsyncTaskTests(BaseTestCase):

    def test_publish_progress(self):
        test = MockAsyncTask()
        test.execute()

        self.assertTrue(False, "Not implemented")

    def test_cancel(self):

        class CancelObserver(Observer):
            def __init__(self, test_case):
                Observer.__init__(self)
                self.test_case = test_case

            def update(self, result, update_code=0):
                if update_code == AsyncTask.STATUS_CODE_CANCEL:
                    self.test_case.assertTrue(True)
                elif update_code == AsyncTask.STATUS_CODE_COMPLETE:
                    self.test_case.assertFalse(True, "Async Task did not Cancel during its running operation")
                else:
                    self.test_case.assertTrue(update_code = AsyncTask.STATUS_CODE_PROGRESS)

        test = MockAsyncTask()
        observer = CancelObserver(self)
        test.attach(observer)
        test.execute()
        sleep(0.002)
        test.on_cancel(True)
        sleep(0.008)



    def test_is_cancelled(self):
        self.assertTrue(False, "Not implemented")

    def test_execute(self):
        self.assertTrue(False, "Not implemented")


class ObserverAsyncTaskTests(BaseTestCase):
    def test_on_progress_update(self):
        self.assertTrue(False, "Not implemented")

    def test_on_post_execute(self):
        self.assertTrue(False, "Not implemented")

