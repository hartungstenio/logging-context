from .context import execution_context


class LoggingContext:
    def __init__(self, **data):
        self.data = data

    def __enter__(self):
        execution_context.push_context(self.data)

    def __exit__(self, *args, **kwargs):
        execution_context.pop_context()
