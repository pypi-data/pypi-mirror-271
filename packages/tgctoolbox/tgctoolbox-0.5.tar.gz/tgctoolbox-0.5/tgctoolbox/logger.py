import inspect
import logging
from typing import Type


class JacobsAmazingLoggerFormatter(logging.Formatter):
    """Logging Formatter to add colors to the levelname and include function name"""

    grey = "\x1b[38;21m"
    blue = "\x1b[34m"
    light_blue = "\x1b[94m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    red = "\x1b[31m"
    reset = "\x1b[0m"

    LEVEL_COLORS = {
        logging.DEBUG: blue,
        logging.INFO: green,
        logging.WARNING: yellow,
        logging.ERROR: red,
        logging.CRITICAL: red,
    }

    def format(self, record):
        # Dynamically find the name of the calling function
        stack = inspect.stack()
        func_name = "unknown"
        for frame in stack:
            if (
                frame.function not in ["emit", "format"]
                and "logging" not in frame.filename
            ):
                func_name = frame.function
                break
        record.func_name = func_name

        # Colorize levelname
        color = self.LEVEL_COLORS.get(record.levelno, self.grey)
        record.levelname = color + record.levelname + self.reset

        if hasattr(record, "timespec"):
            record.msg = self.light_blue + "TIMESPEC: " + self.reset + record.msg
            return super(JacobsAmazingLoggerFormatter, self).format(record)

        if hasattr(record, "result"):
            record.msg = self.light_blue + "RESULT: " + self.reset + record.msg
            return super(JacobsAmazingLoggerFormatter, self).format(record)

        # Set the format and return the formatted record
        self._style._fmt = "%(levelname)s: [%(func_name)s] %(asctime)s - %(message)s"
        return super(JacobsAmazingLoggerFormatter, self).format(record)


class JacobsAmazingLogger(logging.Logger):
    def timespec(self, message, *args, **kwargs):
        # Add a custom attribute to the log record
        if self.isEnabledFor(logging.INFO):
            # Create a new record with a custom attribute
            record = self.makeRecord(
                self.name,
                logging.INFO,
                "(unknown file)",
                0,
                message,
                args,
                kwargs,
                None,
            )
            record.timespec = True
            self.handle(record)


class JacobsAmazingResultsLogger(logging.Logger):
    def result(self, message, *args, **kwargs):
        # Add a custom attribute to the log record
        if self.isEnabledFor(logging.INFO):
            # Create a new record with a custom attribute
            record = self.makeRecord(
                self.name,
                logging.INFO,
                "(unknown file)",
                0,
                message,
                args,
                kwargs,
                None,
            )
            record.result = True
            self.handle(record)


def setup_custom_logger(
    name: str, level: str = "INFO", logger=None
) -> Type[logging.Logger]:
    """
    Set up and return a custom logger with the specified name and level.

    :param name: Name of the logger.
    :param level: Logging level, e.g., 'INFO', 'DEBUG'.
    :return: Configured logger instance.
    """
    if logger is not None:
        logger = logger
    else:
        logger = logging.getLogger(name)
    logger.setLevel(level.upper())

    # Create and set handler and formatter
    handler = logging.StreamHandler()
    handler.setFormatter(JacobsAmazingLoggerFormatter())
    logger.addHandler(handler)

    return logger


def log_result(message):
    logger = setup_custom_logger(
        __name__, level="INFO", logger=JacobsAmazingResultsLogger(__name__)
    )
    logger.result(message)
