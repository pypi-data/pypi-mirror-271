import logging
import sys
from abc import ABC


class WithLogging(ABC):
    def __init__(self, log_file=None, level=logging.INFO) -> None:
        formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        logger = logging.getLogger()
        # while len(logger.handlers) > 0:
        #     logger.handlers.pop()
        logger.setLevel(level)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        if log_file is not None:
            handler = logging.FileHandler(log_file)
            handler.setLevel(level)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
