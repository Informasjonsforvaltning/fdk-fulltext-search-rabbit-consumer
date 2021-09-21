import os
from pythonjsonlogger import jsonlogger
from typing import Any, Dict

RABBITMQ = {
    'USERNAME': os.getenv("RABBIT_USERNAME", "admin"),
    'PASSWORD': os.getenv("RABBIT_PASSWORD", "admin"),
    'HOST': os.getenv("RABBIT_HOST", "localhost")
}

FULLTEXT_SEARCH = {
    'BASE_URL': os.getenv('FDK_FULLTEXT_SEARCH_BASE_URL', 'http://localhost:5000'),
    'API_KEY': os.getenv('FDK_FULLTEXT_API_KEY', 'test-key')
}

LOGGING = {
    'LEVEL': os.getenv('LOG_LEVEL', 'INFO')
}


class StackdriverJsonFormatter(jsonlogger.JsonFormatter, object):
    """json log formatter."""

    def __init__(
            self: Any,
            fmt: str = "%(levelname) %(message)",
            style: str = "%",
            *args: Any,
            **kwargs: Any
    ) -> None:
        jsonlogger.JsonFormatter.__init__(self, fmt=fmt, *args, **kwargs)

    def process_log_record(self: Any, log_record: Dict) -> Any:
        log_record["severity"] = log_record["levelname"]
        del log_record["levelname"]
        log_record["serviceContext"] = {"service": "fdk-fulltext-search"}
        return super(StackdriverJsonFormatter, self).process_log_record(log_record)