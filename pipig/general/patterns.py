from abc import ABCMeta, abstractmethod
import threading
import time

class Subject(object):
    """
    Base Object to notify observers
    """

    def __init__(self):
        self._observers = []

    def attach(self, observer):
        """
        Attach an observer to allow for Notifications
        :param observer: Object which will listen for Notifications
        :return: None
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer=None):
        """
        Detach an observer to allow for Notifications
        :param observer: Object which will listen for Notifications
        :return: None
        """
        if observer is None:
            self._observers = []
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, result, status_code=None):
        """
        Notify all observers of the result
        :param result:
        :return:
        """
        for observer in self._observers:
            observer.update(result, update_code=status_code)


class Observer:
    """
    Attaches to a Subject to be notified by it
    """

    def __init__(self):
        pass

    @abstractmethod
    def update(self, result, update_code=0):
        """
        Abstract Method to implement once it has been notified by its Subject
        :param update_code: Identify the Notifyer code
        :param result: The payload of the Notifyer
        :return:
        """
        raise NotImplementedError


class AsyncThread(threading.Thread):
    """
    Manages the active Thread lifecycle during an AsyncTask
    """
    async_task = None
    params = None

    def __init__(self, async_task, params):
        threading.Thread.__init__(self)
        self.async_task = async_task
        self.params = params

    def run(self):
        """
        Triggered by the start() method of the Thread.
        Manage the Threaded components of the AsyncTask methods
        """
        result = self.async_task.on_operation(self.params)
        self.async_task.on_post_execute(result)


class AsyncTask(Subject):
    """
    Task to run in a background Thread.

    This is a base class to override with specific implementations.
    Examples - Getting Sensor readings without blocking the main Thread

    Start this task with the execute() method
    Has the function to update the main Thread with the tasks progress
    Has the function to update the main Thread at the end of the task
    Has the function to call cancel() to interrupt a task
    """
    __metaclass__ = ABCMeta

    async_thread = None
    params = None

    STATUS_CODE_PRE_EXECUTE = 1
    STATUS_CODE_PROGRESS = 2
    STATUS_CODE_COMPLETE = 3
    STATUS_CODE_CANCEL = 4

    def __init__(self):
        super(AsyncTask, self).__init__()
        self.cancel_flag = False

    # ___________________________________________________________________________
    #
    # TEMPLATE PATTERN USER METHODS
    # ___________________________________________________________________________

    def pre_execute(self, payload=None):
        return payload

    @abstractmethod
    def operation(self, params=None):
        raise NotImplementedError

    def progress(self, payload=None):
        """
        invoked on the UI thread after a call to publishProgress(Progress...).
        The timing of the execution is undefined.
        This method is used to display any form of payload in the user interface while the background computation is still executing.
        For instance, it can be used to animate a payload bar or show logs in a text field.
        """
        return payload

    def complete(self, payload=None):
        return payload

    def cancel(self, payload=None):
        return payload

    # ___________________________________________________________________________
    #
    # TEMPLATE PATTERN MACHINE METHODS
    # ___________________________________________________________________________

    def execute(self, params=None):
        """

        Execute must be invoked on the UI thread.

        Runs this sequence of events:
            on_pre_execute()
            start a new thread
            call do_in_background() on thread
            call on_post_execute() once do_in_background() is finished

            can be interupted by cancel() which will call the on_cancelled() method

        """
        self.async_thread = AsyncThread(self, params)
        self.params = params
        self.on_pre_execute()

        self.async_thread.start()

    def on_pre_execute(self):
        """
        invoked on the UI thread before the task is executed.
        This step is normally used to setup the task, for instance by showing a progress bar in the user interface.
        """
        self.notify(result=self.pre_execute(), status_code=self.STATUS_CODE_PRE_EXECUTE)

    def on_operation(self, params):
        """
        invoked on the background thread immediately after onPreExecute() finishes executing.
        This step is used to perform background computation that can take a long time.
        The parameters of the asynchronous task are passed to this step.
        The result of the computation must be returned by this step and will be passed back to the last step.
        This step can also use publishProgress(Progress...) to publish one or more units of progress.
        These values are published on the UI thread, in the onProgressUpdate(Progress...) step.
        """
        operation_result = self.operation(params)
        return operation_result

    def on_progress(self, progress):
        """
        Call from within do_in_background to trigger on_progress_update abstract method
        """
        self.notify(self.progress(progress), self.STATUS_CODE_PROGRESS)

    def on_post_execute(self, result):
        """
        invoked on the UI thread after the background computation finishes.
        The result of the background computation is passed to this step as a parameter.
        """

        self.notify(result, self.STATUS_CODE_COMPLETE)

    def is_cancelled(self, payload):
        """
        Returns the state of the 'Cancel Flag'

        Insert into 'Operation' code to check status of flag. Often use after each cycle of a loop
        """
        if self.cancel_flag:
            self.notify(result=self.cancel(payload), status_code=self.STATUS_CODE_CANCEL)
        return self.cancel_flag

    def on_cancel(self):
        """
        A task can be cancelled at any time by invoking cancel(boolean).
        Invoking this method will cause subsequent calls to isCancelled() to return true.
        After invoking this method, onCancelled(Object),
            instead of onPostExecute(Object) will be invoked after doInBackground(Object[]) returns.
        To ensure that a task is cancelled as quickly as possible,
            you should always check the return value of isCancelled() periodically from doInBackground(Object[]),
            if possible (inside a loop for instance.)
        """
        self.cancel_flag = True


class TestAsy(AsyncTask):
    def cancel(self, payload=None):
        pass

    def progress(self, payload=None):
        pass

    def operation(self, params=None):
        return "Test"


class ObserverAsyncTask(AsyncTask, Subject):
    def __init__(self):
        AsyncTask.__init__(self)
        Subject.__init__(self)

    def progress(self, payload):
        self.notify(payload)

    def on_post_execute(self, result):
        self.notify(result)












class BasicAsyncTask(AsyncTask):
    """
    Not used in final code. This is a testing object to experiment with
    """
    counter = 0

    def on_pre_execute(self):
        self.counter = 0

    def on_operation(self, params):
        for i in range(0, 10):
            if self.is_cancelled():
                return self.on_cancel(("I cancelled counting ", self.counter, params))
            self.counter += 1
            self.on_progress(("Counting ", self.counter, params))
            time.sleep(0.5)
        return "counted", self.counter, params

    def on_post_execute(self, result):
        if result is None:
            print "BasicAsyncTask is Complete with result: None"
        message = "BasicAsyncTask is Complete with result: " + str(result[0]) + " " + str(result[1]) + " " + str(result[2])
        print message
        return message

    def progress(self, payload):
        message = "BasicAsyncTask Progress: " + str(payload[0]) + " " + str(payload[1]) + " " + str(payload[2])
        print message
        return message

    def on_cancel(self, payload):
        message = "BasicAsyncTask cancelled with payload: " + str(payload[0]) + " " + str(payload[1]) + " " + str(payload[2])
        print message
        return payload
        # return message

if __name__ == '__main__':
    task = BasicAsyncTask()
    task.execute("Chickens")
    time.sleep(1)
    task.cancel(True)

    # BasicAsyncTask Progress: Counting  1 Chickens
    # BasicAsyncTask Progress: Counting  2 Chickens
    # BasicAsyncTask cancelled with result: I cancelled counting  2 Chickens
    # BasicAsyncTask is Complete with result: I cancelled counting  2 Chickens
