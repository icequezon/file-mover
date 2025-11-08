import logging
import inspect


class AppLogger:
    """
    A wrapper around Python's built-in logging that:
    - Adds timestamps
    - Includes the name of the calling function
    - Supports multiple log levels
    """

    def __init__(
        self, name: str = __name__, log_file: str = None, level: int = logging.DEBUG
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False  # Prevent duplicate logs in some environments

        # Define log format: timestamp, level, function name, message
        log_format = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(funcName)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_format)
        self.logger.addHandler(console_handler)

        # Optional file handler
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(log_format)
            self.logger.addHandler(file_handler)

    def _get_caller(self):
        """Return the name of the function that called the logger method."""
        stack = inspect.stack()
        # index 2 because: _get_caller -> log method -> actual caller
        if len(stack) > 2:
            return stack[2].function
        return "<module>"

    def debug(self, message: str):
        self.logger.debug(f"{self._get_caller()}: {message}")

    def info(self, message: str):
        self.logger.info(f"{self._get_caller()}: {message}")

    def warning(self, message: str):
        self.logger.warning(f"{self._get_caller()}: {message}")

    def error(self, message: str):
        self.logger.error(f"{self._get_caller()}: {message}")

    def critical(self, message: str):
        self.logger.critical(f"{self._get_caller()}: {message}")


logger = AppLogger("file-mover")
