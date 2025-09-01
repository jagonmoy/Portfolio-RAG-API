import logging
import sys
from typing import Any, Dict


def setup_logging(log_level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("app.log", mode="a"),
        ],
    )

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

    def info(self, message: str, **kwargs: Dict[str, Any]) -> None:
        extra_data = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
        log_message = f"{message} | {extra_data}" if extra_data else message
        self.logger.info(log_message)

    def error(self, message: str, **kwargs: Dict[str, Any]) -> None:
        extra_data = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
        log_message = f"{message} | {extra_data}" if extra_data else message
        self.logger.error(log_message)

    def warning(self, message: str, **kwargs: Dict[str, Any]) -> None:
        extra_data = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
        log_message = f"{message} | {extra_data}" if extra_data else message
        self.logger.warning(log_message)
