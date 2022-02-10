import logging

from .context import execution_context


class LoggingContext:
    def __init__(self, **data):
        self.data = data

    def __enter__(self):
        current_record_factory = logging.getLogRecordFactory()

        throwaway_record = current_record_factory(
            __name__, logging.DEBUG, __file__, 14, "test_msg", [], None
        )
        if not hasattr(throwaway_record, "logging_context"):
            from logging_context import logging as ctx_logging

            new_factory = ctx_logging.log_record_factory(current_record_factory)
            logging.setLogRecordFactory(new_factory)

        execution_context.push_context(self.data)

    def __exit__(self, *args, **kwargs):
        execution_context.pop_context()
