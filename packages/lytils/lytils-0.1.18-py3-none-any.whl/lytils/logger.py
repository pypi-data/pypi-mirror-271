import logging
from inspect import currentframe
from lytils import ctext
from lytils.file import LyFile


def get_line_number():
    cf = currentframe()
    return cf.f_back.f_lineno


class InvalidLogLevelException(Exception):
    # Raise this when undetected_chromedriver is not installed
    def __init__(
        self,
        message=f"<y>Parameter 'level' must equal one of the following: debug, info, warning, error, critical.",
    ):
        self.message = ctext(message)
        super().__init__(self.message)


class LyLoggerNotSetUpException(Exception):
    # Raise this when undetected_chromedriver is not installed
    def __init__(
        self,
        message=f"<y>LyLogger.setup() not ran.",
    ):
        self.message = ctext(message)
        super().__init__(self.message)


class LyLogger:
    LEVELS = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    def __init__(
        self,
        name: str,
        path: str = "",
        persistent: bool = False,
        encoding: str = "utf-8",
        formatting: str = "%(asctime)s - [%(levelname)s] %(message)s",
        date_format: str = "%Y-%m-%d %H:%M:%S",
        level="warning",
        debug_path: str = "",
        info_path: str = "",
        warning_path: str = "",
        error_path: str = "",
        critical_path: str = "",
    ):
        """
        Wrapper around the 'logging' package.

        Args:
            name (str): Each instance of logging needs a name to associate its handlers.
            path (str): The default path of the log file(s). Defaults to 'logs/{name}.log'.
            persistent (bool): Set to True if log file(s) should not be overwritten.
            encoding (str): The encoding of the log file(s).
            formatting (str): The formatting of the prefix for each line in the log file(s).
            date_format (str): The date format of the timestamp for each line in the log file(s).
            level (str): The importance level of messages to be shown. Least to most: debug > info > warning > error > critical.
            debug_path (str): The path of the debug logs (ex. file.debug.log). Defaults to path.
            info_path (str): The path of the info logs (ex. file.info.log). Defaults to path.
            warning_path (str): The path of the warning logs (ex. file.warning.log). Defaults to path.
            error_path (str): The path of the error logs (ex. file.error.log). Defaults to path.
            critical_path (str): The path of the critical logs (ex. file.critical.log). Defaults to path.
        """
        self.name = name
        self.path = path if path else f"logs/{name}.log"
        self.encoding = encoding
        self.formatting = formatting
        self.date_format = date_format

        if level not in LyLogger.LEVELS.keys():
            raise InvalidLogLevelException
        self.level = LyLogger.LEVELS[level]

        # Allow for multiple log files
        self.debug_path = debug_path if debug_path else self.path
        self.info_path = info_path if info_path else self.path
        self.warning_path = warning_path if warning_path else self.path
        self.error_path = error_path if error_path else self.path
        self.critical_path = critical_path if critical_path else self.path

        self._logger = None
        self.setup(persistent)

    def _get_file_handler(self, path: str, level, formatter):
        file_handler = logging.FileHandler(path)
        file_handler.setLevel(LyLogger.LEVELS[level])
        file_handler.setFormatter(formatter)
        return file_handler

    def setup(self, persistent: bool = False) -> None:
        """
        Set up individual instance of logging.

        Args:
            persistent (bool): Set to True if log file should not be overwritten.

        """
        # Create new log files if they should be overwritten or if it doesn't exist.
        if not persistent or not log_file.exists():
            for path in {
                self.path,
                self.debug_path,
                self.info_path,
                self.warning_path,
                self.error_path,
                self.critical_path,
            }:
                log_file = LyFile(path)
                log_file.create()

        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)

        formatter = logging.Formatter(self.formatting)

        # Get and add file handlers
        debug_handler = self._get_file_handler(self.debug_path, "debug", formatter)
        logger.addHandler(debug_handler)

        info_handler = self._get_file_handler(self.info_path, "info", formatter)
        logger.addHandler(info_handler)

        warning_handler = self._get_file_handler(
            self.warning_path, "warning", formatter
        )
        logger.addHandler(warning_handler)

        error_handler = self._get_file_handler(self.error_path, "error", formatter)
        logger.addHandler(error_handler)

        critical_handler = self._get_file_handler(
            self.critical_path, "critical", formatter
        )
        logger.addHandler(critical_handler)

        self._logger = logger

    def debug(self, message: str):
        """
        Logs message of level: debug.

        Args:
            message (str): Message to log.
        """
        if not self._logger:
            raise LyLoggerNotSetUpException
        self._logger.debug(message)

    def info(self, message: str):
        """
        Logs message of level: info.

        Args:
            message (str): Message to log.
        """
        if not self._logger:
            raise LyLoggerNotSetUpException
        self._logger.info(message)

    def warning(self, message: str):
        """
        Logs message of level: warning.

        Args:
            message (str): Message to log.
        """
        if not self._logger:
            raise LyLoggerNotSetUpException
        self._logger.warning(message)

    def error(self, message: str):
        """
        Logs message of level: error.

        Args:
            message (str): Message to log.
        """
        if not self._logger:
            raise LyLoggerNotSetUpException
        self._logger.error(message)

    def critical(self, message: str):
        """
        Logs message of level: critical.

        Args:
            message (str): Message to log.
        """
        if not self._logger:
            raise LyLoggerNotSetUpException
        self._logger.critical(message)

    def debug_json(self, message: str, data, indent: int = 4):
        """
        Logs message and json of level: debug.

        Args:
            message (str): Message to log.
            data: Json data to log.
            indent (int): Indentation of json data.
        """
        if not self._logger:
            raise LyLoggerNotSetUpException
        self._logger.debug(message)
        file = LyFile(self.debug_path)
        file.append_json(data, indent)

    def info_json(self, message: str, data, indent: int = 4):
        """
        Logs message and json of level: info.

        Args:
            message (str): Message to log.
            data: Json data to log.
            indent (int): Indentation of json data.
        """
        if not self._logger:
            raise LyLoggerNotSetUpException
        self._logger.info(message)
        file = LyFile(self.info_path)
        file.append_json(data, indent)

    def warning_json(self, message: str, data, indent: int = 4):
        """
        Logs message and json of level: warning.

        Args:
            message (str): Message to log.
            data: Json data to log.
            indent (int): Indentation of json data.
        """
        if not self._logger:
            raise LyLoggerNotSetUpException
        self._logger.warning(message)
        file = LyFile(self.warning_path)
        file.append_json(data, indent)

    def error_json(self, message: str, data, indent: int = 4):
        """
        Logs message and json of level: error.

        Args:
            message (str): Message to log.
            data: Json data to log.
            indent (int): Indentation of json data.
        """
        if not self._logger:
            raise LyLoggerNotSetUpException
        self._logger.error(message)
        file = LyFile(self.error_path)
        file.append_json(data, indent)

    def critical_json(self, message: str, data, indent: int = 4):
        """
        Logs message and json of level: critical.

        Args:
            message (str): Message to log.
            data: Json data to log.
            indent (int): Indentation of json data.
        """
        if not self._logger:
            raise LyLoggerNotSetUpException
        self._logger.critical(message)
        file = LyFile(self.critical_path)
        file.append_json(data, indent)
