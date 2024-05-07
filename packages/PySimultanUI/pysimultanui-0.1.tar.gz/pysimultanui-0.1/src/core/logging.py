import logging
from datetime import datetime
from nicegui import ui

logger = logging.getLogger('py_simultan_cfd')


class LogElementHandler(logging.Handler):
    """A logging handler that emits messages to a log element."""

    def __init__(self, element: ui.log, level: int = logging.NOTSET) -> None:
        self.element = element
        super().__init__(level)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self.element.push(msg)
        except Exception:
            self.handleError(record)
