import contextvars
from functools import reduce
from collections import deque
from collections.abc import Mapping, MutableSequence
from typing import Any, MutableMapping

ContextData = Mapping[str, Any]


class LoggingVarsContext:
    logging_context_var: contextvars.ContextVar[
        MutableSequence[ContextData]
    ] = contextvars.ContextVar("logging_context_var")

    def push_context(self, data: dict):
        try:
            current_context = self.logging_context_var.get()
        except LookupError:
            current_context = deque()
            self.logging_context_var.set(current_context)

        current_context.append(data)

    def pop_context(self) -> ContextData | None:
        try:
            current_context = self.logging_context_var.get()
            return current_context.pop()
        except LookupError:
            pass

    def get_current_context(self) -> ContextData:
        def dict_update(a: MutableMapping, b: Mapping):
            a.update(b)
            return a

        try:
            current_context = self.logging_context_var.get()
            return reduce(
                dict_update,
                current_context,
                {"logging_context": len(current_context)},
            )
        except LookupError:
            return {"logging_context": 0}


execution_context = LoggingVarsContext()
