import logging
import sys
import warnings
from vortex.config import LOGGING_LEVEL_STR

# Formatting
FORMATTER = logging.Formatter(
    "[%(name)s][%(levelname)s]: %(asctime)-15s: %(message)s",  # noqa
    datefmt="%m-%d-%y-%I:%M:%S%p",
)

# Logging
ROOT_LOGGER = logging.getLogger("vortex")
LOGGING_LEVEL = getattr(logging, LOGGING_LEVEL_STR)

# ERROR LOGGING
_errorHandler = logging.FileHandler("/var/log/server-error.log")
_errorHandler.setFormatter(FORMATTER)
_errorHandler.setLevel(logging.ERROR)


# STDOUT LOGGING
streamHandler = logging.StreamHandler(sys.stdout)
streamHandler.setFormatter(FORMATTER)

ROOT_LOGGER.addHandler(_errorHandler)
ROOT_LOGGER.addHandler(streamHandler)
ROOT_LOGGER.setLevel(LOGGING_LEVEL)

# Turn down 3rd party logging
logging.getLogger("requests").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)


class Logging(object):
    @classmethod
    def get(cls, name):
        logger = ROOT_LOGGER.getChild(name)
        logger.setLevel(ROOT_LOGGER.level)
        return logger


warnings.filterwarnings("ignore")
