from os import environ as env
from pythonjsonlogger import jsonlogger
from typing import Any, Dict

RABBITMQ = {
    'USERNAME': env.get("RABBIT_USERNAME", "admin"),
    'PASSWORD': env.get("RABBIT_PASSWORD", "admin"),
    'HOST': env.get("RABBIT_HOST", "localhost")
}

FULLTEXT_SEARCH = {
    'BASE_URL': env.get('FDK_FULLTEXT_SEARCH_BASE_URL', 'http://localhost:5000'),
    'API_KEY': env.get('FDK_FULLTEXT_API_KEY', 'test-key')
}

LOGGING = {
    'LEVEL': env.get('LOG_LEVEL', 'INFO')
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
        log_record["serviceContext"] = {"service": "fdk-fulltext-search-rabbit-consumer"}
        return super(StackdriverJsonFormatter, self).process_log_record(log_record)
