from processor_chain import DatabaseProcessorChain, DebugProcessorChain, DatabasePrintProcessorChain

DATABASE_ONLY = 'database'
PRINT_ONLY = 'print'
PRINT_DATABASE = 'print_database'


class ProcessorChainFactory:
    def build_object(self, object_type):
        if object_type == DATABASE_ONLY:

            return DatabaseProcessorChain(1, False)

        elif object_type == PRINT_DATABASE:
            return DatabasePrintProcessorChain(1, False)

        else:
            return DebugProcessorChain(1, False)