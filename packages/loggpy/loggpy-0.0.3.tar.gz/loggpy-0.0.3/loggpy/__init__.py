# Custom log levels for Python's logging module.
#
# Modder: ReiDoBrega
# Last Change: 04/05/2024

"""
Custom log levels for Python's :mod:`logging` module.
"""

import sys
import logging
import verboselogs
from typing import NoReturn, Optional
from rich.logging import RichHandler

NOTICE = 25
SPAM = 5
SUCCESS = 35
VERBOSE = 15
LOGKEY = 21
DEBUG = 10


class Logger(logging.Logger):
    """
    Custom logger class supporting additional logging levels.

    Adds support for `notice()`, `spam()`, `success()`, `verbose()`,
    `logkey()`, and `exit()` methods.
    """

    # Default log format settings
    LOG_FORMAT_CLI = "{name}: {message}"
    LOG_FORMAT_FILE = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    LOG_DATE_FORMAT = '%H:%M:%S' # %H:%M:%S
    LOG_STYLE = "{"

    BLACKLIST = []

    def __init__(self, *args, **kwargs):
        """
        Initialize a Logger object.

        :param args: Arguments passed to superclass (logging.Logger).
        :param kwargs: Keyword arguments passed to superclass (logging.Logger).
        """
        super().__init__(*args, **kwargs)
        self.parent = logging.getLogger()

    @classmethod
    def mount(cls,
              level: int, 
              HandlerFilename: str,
              tracebacks_suppress: list[object],
              blacklist: Optional[list[str]] = []):
        """
        Usage:

            level: int -> The Logging level
            HandlerFilename: str -> The Path of your `logfile.log`
            tracebacks_suppress: list[object] -> a list with some tracebacks for the Handler, ex: [cloup, click, httpx]
        """
        if blacklist:
            cls.BLACKLIST = blacklist

        # * CONFIGURE LOGGING TO WRITE TO A FILE
        handler = logging.FileHandler(HandlerFilename, encoding="utf-8")
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter(cls.LOG_FORMAT_FILE))
        logging.basicConfig(
            level=logging.DEBUG,
            format=cls.LOG_FORMAT_CLI,
            datefmt=cls.LOG_DATE_FORMAT,
            style=cls.LOG_STYLE,
            handlers=[
                RichHandler(
                    level=level,
                    rich_tracebacks=True,
                    tracebacks_show_locals=True,
                    show_path=True if level in [DEBUG, VERBOSE] else False,
                    markup=True,
                    tracebacks_suppress=tracebacks_suppress,
                ),
                handler,
            ],
        )
        verboselogs.install()

    def log(self, level: int, msg: object, *args: object, **kwargs) -> None:
        """
        Log a message with the specified level.

        Adjusts log level based on logger name and message content.
        """
        if self.name in self.BLACKLIST:
            level = logging.DEBUG
        if self.name.startswith("seleniumwire") and level <= logging.INFO:
            level = logging.DEBUG

        if self.name.startswith("urllib3"):
            if msg.startswith("Incremented Retry"):
                level = logging.WARNING
            elif level == logging.DEBUG:
                level = VERBOSE

            if msg == '%s://%s:%s "%s %s %s" %s %s':
                scheme, host, port, method, url, protocol, status, reason = args
                if (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
                    msg = "%s %s://%s%s %s %s %s"
                    args = (method, scheme, host, url, protocol, status, reason)
                else:
                    msg = "%s %s://%s:%s%s %s %s %s"
                    args = (method, scheme, host, port, url, protocol, status, reason)

        super().log(level, msg, *args, **kwargs)

    def notice(self, msg, *args, **kwargs) -> None:
        """Log a message with level NOTICE."""
        if self.isEnabledFor(NOTICE):
            self.log(NOTICE, msg, *args, **kwargs)

    def spam(self, msg, *args, **kwargs) -> None:
        """Log a message with level SPAM."""
        if self.isEnabledFor(SPAM):
            self.log(SPAM, msg, *args, **kwargs)

    def success(self, msg, *args, **kwargs) -> None:
        """Log a message with level SUCCESS."""
        if self.isEnabledFor(SUCCESS):
            self.log(SUCCESS, msg, *args, **kwargs)

    def verbose(self, msg, *args, **kwargs) -> None:
        """Log a message with level VERBOSE."""
        if self.isEnabledFor(VERBOSE):
            self.log(VERBOSE, msg, *args, **kwargs)

    def logkey(self, msg, *args, **kwargs) -> None:
        """Log a message with level LOGKEY."""
        if self.isEnabledFor(LOGKEY):
            self.log(LOGKEY, msg, *args, **kwargs)

    def exit(self, msg, *args, **kwargs) -> NoReturn:
        """
        Log a message with severity 'CRITICAL' and terminate the program.

        :param msg: The message to log.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """
        self.critical(msg, *args, **kwargs)
        sys.exit(1)

# Define custom log levels
for level, name in [
    (NOTICE, 'NOTICE'),
    (SPAM, 'SPAM'),
    (SUCCESS, 'SUCCESS'),
    (VERBOSE, 'VERBOSE'),
    (LOGKEY, 'LOGKEY')
]:
    logging.addLevelName(level, name)
    setattr(logging, name, level)


__all__ = [
    'Logger', 'install', 'logging'
]


__version__ = '0.0.3'
