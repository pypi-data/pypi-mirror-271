import inspect
import logging
from enum import Enum

from pathier import Pathier, Pathish

from loggi import models

root = Pathier(__file__).parent


class Logger(logging.Logger):
    @property
    def logpath(self) -> Pathier | None:
        """Return a file handler path whose stem matches `self.name`, if there is one."""
        for path in self.logpaths:
            if path.stem == self.name:
                return path

    @property
    def logpaths(self) -> list[Pathier]:
        """A list of `Pathier` objects for any file handlers attached to this `Logger`."""
        return [
            Pathier(handler.baseFilename)
            for handler in self.handlers
            if isinstance(handler, logging.FileHandler)
        ]

    def close(self):
        """Remove and close this logger's handlers."""
        for handler in self.handlers:
            self.removeHandler(handler)
            handler.close()

    def get_log(self) -> models.Log | None:
        """Returns a `models.Log` object populated from this logger's `logpath`."""
        if path := self.logpath:
            return models.Log.load_log(path)

    def logprint(self, message: str, level: str | int = "INFO"):
        """Log and print `message`.

        Only prints if the logger is enabled for the give `level`."""
        getattr(
            self,
            (level if isinstance(level, str) else logging.getLevelName(level)).lower(),
        )(message)
        if self.isEnabledFor(
            level if isinstance(level, int) else logging.getLevelName(level)
        ):
            print(message)


def getLogger(name: str, path: Pathish = Pathier.cwd()) -> Logger:
    """Get a configured `loggi.Logger` instance for `name` with a file handler.

    The log file will be located in `path` at `path/{name}.log`.

    Default level is `INFO`.

    Logs are in the format: `{levelname}|-|{asctime}|-|{message}

    asctime is formatted as `%x %X`"""
    path = Pathier(path)
    path.mkdir()
    # make sure loggi.Logger is the current logger class
    logging.setLoggerClass(Logger)
    logger = logging.Logger.manager.getLogger(name)
    # TODO: Add option for a stream handler
    # Add file handler using `logger.name`
    logpath = path / f"{logger.name}.log"
    handler = logging.FileHandler(logpath, encoding="utf-8")
    if handler.baseFilename not in [
        existing_handler.baseFilename
        for existing_handler in logger.handlers
        if isinstance(existing_handler, logging.FileHandler)
    ]:
        handler.setFormatter(
            logging.Formatter(
                "{levelname}|-|{asctime}|-|{message}", style="{", datefmt="%x %X"
            )
        )
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger  # type: ignore


def load_log(logpath: Pathish) -> models.Log:
    """Return a `loggi.models.Log` object for the log file at `logpath`."""
    return models.Log.load_log(Pathier(logpath))


class LogName(Enum):
    CLASSNAME = 1
    FILENAME = 2


class LoggerMixin:
    """Inherit from this class and call `self.init_logger()` in your `__init__()` function.

    The logger instance can then be accessed through `self.logger`."""

    def init_logger(
        self,
        name: str | int | LogName = LogName.CLASSNAME,
        log_dir: Pathish = "logs",
        log_level: int | str = "INFO",
    ):
        """
        Initialize the logger instance.

        #### :params:
        * `name`: The name for the logger. The log file will be named `{name}.log`.
        If `LogName.CLASSNAME` is given, a lowercase version of the name of the inheriting class will be used.
        If `LogName.FILENAME` is given, a lowercase version of the file stem the inheriting class is instantiated in will be used.
        * `log_dir`: The directory the log file will be written to.
        * `log_level`: The level for the logger.
        """
        log_dir = Pathier(log_dir)
        if name == LogName.CLASSNAME:
            name = self.__class__.__name__.lower()
        elif name == LogName.FILENAME:
            source_file = inspect.getsourcefile(type(self))
            if source_file:
                name = Pathier(source_file).stem
            else:
                name = Pathier(__file__).stem
            name = name.lower()
        name = str(name)
        self.logger = getLogger(name, log_dir)
        self.logger.setLevel(log_level)


# |===================================================|
# Backwards compatibility with previous loggi versions
# |===================================================|


def get_logpaths(logger: Logger | logging.Logger) -> list[Pathier]:
    """Loop through the handlers for `logger` and return a list of paths for any handler of type `FileHandler`."""
    return [
        Pathier(handler.baseFilename)
        for handler in logger.handlers
        if isinstance(handler, logging.FileHandler)
    ]


def get_logpath(logger: Logger | logging.Logger) -> Pathier | None:
    """Search `logger.handlers` for a `FileHandler` that has a file stem matching `logger.name`.

    Returns `None` if not found."""
    for path in get_logpaths(logger):
        if path.stem == logger.name:
            return path


def get_log(logger: Logger | logging.Logger) -> models.Log | None:
    """Find the corresponding log file for `logger`, load it into a `models.Log` instance, and then return it.

    Returns `None` if a log file can't be found."""
    path = get_logpath(logger)
    if path:
        return load_log(path)


def close(logger: Logger | logging.Logger):
    """Removes and closes handlers for `logger`."""
    for handler in logger.handlers:
        logger.removeHandler(handler)
        handler.close()
