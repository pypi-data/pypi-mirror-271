import logging
import colorlog
from time import time

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.logger = logging.getLogger(__name__)
            log_handler = colorlog.StreamHandler()
            log_handler.setFormatter(
                colorlog.ColoredFormatter(
                    "%(log_color)s%(levelname)s:%(name)s:%(message)s",
                    log_colors={
                        "DEBUG": "cyan",
                        "INFO": "white",
                        "WARNING": "yellow",
                        "ERROR": "red",
                        "CRITICAL": "red,bg_white",
                    },
                )
            )
            cls._instance.logger = colorlog.getLogger(__name__)
            cls._instance.logger.addHandler(log_handler)
            cls._instance.logger.setLevel(logging.WARNING)

        return cls._instance
    
    def set_log_level(cls, loglevel):
        if loglevel == 1:
                cls._instance.logger.setLevel(logging.ERROR)
        elif loglevel == 2:
            cls._instance.logger.setLevel(logging.INFO)
        elif loglevel == 3:
            cls._instance.logger.setLevel(logging.DEBUG)

