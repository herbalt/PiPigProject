from general.patterns import Observer, Subject
from processors import ProcessorPrint, ProcessorDatabase, ProcessorAverageDelay, BaseProcessor
from abc import abstractmethod, ABCMeta
from utilities import debug_messenger

class ProcessorChain(Observer, Subject):

    __metaclass__ = ABCMeta

    def __init__(self, delay_quantity=1, average=False):
        Observer.__init__(self)
        Subject.__init__(self)
        self.delay_processor = None
        self.create_chain(delay_quantity, average)

    def create_delay_processor(self,  delay_quantity=1, average=False):
        self.delay_processor = ProcessorAverageDelay(delay_quantity=delay_quantity, average=average)
        return self.delay_processor

    def receive(self, payload, status_code=0):
        """
        Method that is called when a Subject notifys its observers
        :param payload:
        :param status_code:
        :return:
        """
        # debug_messenger("RECEIVE PROCESSOR CHAIN: " + str(payload))
        if payload is not None:
            result = self.delay_processor.receive(payload, status_code)
        # self.notify(result, status_code)

    def create_chain(self, delay_quantity=1, average=False):
        self.create_delay_processor(delay_quantity, average)
        processor_objects = self.list_of_processors()

        for processor_object in processor_objects:
            self.delay_processor.attach(processor_object)

    def attach(self, observer):
        # debug_messenger("ATTACH PROCESSOR CHAIN: " + str(observer))
        self.delay_processor.attach(observer)

    @abstractmethod
    def list_of_processors(self):
        """
        A list of all the Processor objects that is to be attached to the delay processor
        :return: 
        """
        return []


class DebugProcessorChain(ProcessorChain):
    def __init__(self, delay_quantity=1, average=False):
        super(DebugProcessorChain, self).__init__(delay_quantity=delay_quantity, average=average)

    def list_of_processors(self):
        processor_print = ProcessorPrint()
        return [processor_print]


class DatabaseProcessorChain(ProcessorChain):
    def __init__(self, delay_quantity=1, average=False):
        super(DatabaseProcessorChain, self).__init__(delay_quantity=delay_quantity, average=average)

    def list_of_processors(self):
        processor_database = ProcessorDatabase()
        return [processor_database]


class DatabasePrintProcessorChain(ProcessorChain):
    def __init__(self, delay_quantity=1, average=False):
        super(DatabasePrintProcessorChain, self).__init__(delay_quantity=delay_quantity, average=average)

    def list_of_processors(self):
        processor_print = ProcessorPrint()
        processor_database = ProcessorDatabase()
        return [processor_print, processor_database]