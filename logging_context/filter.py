import logging

from .context import execution_context


class LoggingContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        data = execution_context.get_current_context()

        for key, value in data.items():
            if (key in ["message", "asctime"]) or (key in record.__dict__):
                continue
            record.__dict__[key] = value

        return super().filter(record)
