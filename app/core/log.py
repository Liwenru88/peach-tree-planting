import logging.config
import os
import uuid
from contextvars import ContextVar
from typing import Optional

from app import settings

request_id_var: ContextVar[Optional[str]] = ContextVar("request_id", default=None)


def request_id_generator() -> str:
    return str(uuid.uuid4())


class RequestIdFilter(logging.Filter):
    def __init__(self, name: str = "", default_value: Optional[str] = None) -> None:
        super().__init__(name)
        self.default_value = default_value

    def filter(self, record: logging.LogRecord):
        record.request_id = request_id_var.get(self.default_value)
        return True



LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s [%(request_id)s] %(name)s %(message)s",
        },
    },
    "filters": {
        "request_id": {
            "()": RequestIdFilter,
            "default_value": "-",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": settings.LOG_LEVEL,
            "formatter": "default",
            "filters": ["request_id"]
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": settings.LOG_LEVEL,
            "formatter": "default",
            "filename": os.path.join(settings.LOG_DIR, "app.log"),
            "when": "D",
            "filters": ["request_id"]
        },
    },
    "root": {
        "level": settings.LOG_LEVEL,
        "handlers": ["console", "file"],
    },
}

if not os.path.exists(settings.LOG_DIR):
    os.makedirs(settings.LOG_DIR)

logging.config.dictConfig(LOGGING)
