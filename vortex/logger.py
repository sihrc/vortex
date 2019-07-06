import logging
import sys
import warnings


# Formatting
FORMATTER = logging.Formatter(
    "[%(name)s][%(levelname)s]: %(asctime)-15s %(filename)s:%(lineno)d Message: %(message)s",  # noqa
    datefmt="%m-%d-%y-%I:%M:%S%p",
)

# Logging
ROOT_LOGGER = logging.getLogger("server")
ROOT_LOGGER.setLevel(logging.DEBUG)

# ERROR LOGGING
errorHandler = logging.FileHandler("/var/log/server-error.log")
errorHandler.setFormatter(FORMATTER)
errorHandler.setLevel(logging.WARNING)

# VERBOSE LOGGING
verboseHandler = logging.FileHandler("/var/log/verbose-server.log")
verboseHandler.setFormatter(FORMATTER)
verboseHandler.setLevel(logging.DEBUG)

# STDOUT LOGGING
streamHandler = logging.StreamHandler(sys.stdout)
streamHandler.setFormatter(FORMATTER)
streamHandler.setLevel(logging.INFO)

ROOT_LOGGER.addHandler(errorHandler)
ROOT_LOGGER.addHandler(verboseHandler)
ROOT_LOGGER.addHandler(streamHandler)

# Turn down 3rd party logging
logging.getLogger("requests").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)


class Logging(object):
    @classmethod
    def getLogger(cls, name):
        logger = ROOT_LOGGER.getChild(name)
        logger.level = logging.DEBUG
        logger.propagate = True
        return logger


warnings.filterwarnings("ignore")
