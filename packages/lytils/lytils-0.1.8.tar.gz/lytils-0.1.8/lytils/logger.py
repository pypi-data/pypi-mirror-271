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
        path: str,
        encoding: str = "utf-8",
        format: str = "%(asctime)s - [%(levelname)s] %(message)s",
        date_format: str = "%Y-%m-%d %H:%M:%S",
        level="debug",
        debug_path: str = "",
        info_path: str = "",
        warning_path: str = "",
        error_path: str = "",
        critical_path: str = "",
    ):
        self._name = name
        self._path = path
        self._encoding = encoding
        self._format = format
        self._date_format = date_format

        if level not in LyLogger.LEVELS.keys():
            raise InvalidLogLevelException
        self._level = LyLogger.LEVELS[level]

        # Allow for multiple log files
        self._debug_path = debug_path if debug_path else path
        self._info_path = info_path if info_path else path
        self._warning_path = warning_path if warning_path else path
        self._error_path = error_path if error_path else path
        self._critical_path = critical_path if critical_path else path

        self._logger = None

    def _get_file_handler(self, path: str, level, formatter):
        file_handler = logging.FileHandler(path)
        file_handler.setLevel(LyLogger.LEVELS[level])
        file_handler.setFormatter(formatter)
        return file_handler

    def setup(self, overwrite: bool = False):
        log_file = LyFile(self._path)

        # Create file if it doesn't exist or we wish to overwrite the log each run.
        if overwrite:
            log_file.create()
        elif not log_file.exists():
            log_file.create()

        logger = logging.getLogger(self._name)
        logger.setLevel(self._level)

        formatter = logging.Formatter(self._format)

        # Get and add file handlers
        debug_handler = self._get_file_handler(self._debug_path, "debug", formatter)
        logger.addHandler(debug_handler)

        info_handler = self._get_file_handler(self._info_path, "info", formatter)
        logger.addHandler(info_handler)

        warning_handler = self._get_file_handler(
            self._warning_path, "warning", formatter
        )
        logger.addHandler(warning_handler)

        error_handler = self._get_file_handler(self._error_path, "error", formatter)
        logger.addHandler(error_handler)

        critical_handler = self._get_file_handler(
            self._critical_path, "critical", formatter
        )
        logger.addHandler(critical_handler)

        self._logger = logger

    def debug(self, message: str):
        if not self._logger:
            raise LyLoggerNotSetUpException
        self._logger.debug(message)

    def info(self, message: str):
        if not self._logger:
            raise LyLoggerNotSetUpException
        self._logger.info(message)

    def warning(self, message: str):
        if not self._logger:
            raise LyLoggerNotSetUpException
        self._logger.warning(message)

    def error(self, message: str):
        if not self._logger:
            raise LyLoggerNotSetUpException
        self._logger.error(message)

    def critical(self, message: str):
        if not self._logger:
            raise LyLoggerNotSetUpException
        self._logger.critical(message)
