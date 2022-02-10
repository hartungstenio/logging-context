from functools import wraps

from .context import execution_context


def _add_logging_context_to_log_record(record):
    data = execution_context.get_current_context()

    for key in data:
        if (key in ["message", "asctime"]) or (key in record.__dict__):
            raise KeyError("Attempt to overwrite %r in LogRecord" % key)
        record.__dict__[key] = data[key]

    return record


def log_record_factory(current_factory):
    """
    Wrap the Python log record factory and add the current context.

    :return:
        LogRecord object, with the current logging context vars
    """

    @wraps(current_factory)
    def wrapper(*args, **kwargs):
        record = current_factory(*args, *kwargs)
        return _add_logging_context_to_log_record(record)

    return wrapper
