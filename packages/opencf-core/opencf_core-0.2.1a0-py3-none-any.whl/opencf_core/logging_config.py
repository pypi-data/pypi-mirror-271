import logging
import os
from datetime import datetime
from typing import Optional


class LoggerConfig:
    def __init__(self) -> None:
        self.logger: logging.Logger = logging.Logger("_")
        self.log_file: Optional[str] = None
        self.log_level: int = logging.INFO

    def setup_logger(
        self, name: str, log_file: Optional[str] = None, level: int = logging.INFO
    ) -> None:
        """Set up logger.

        Args:
            name (str): Name of the logger.
            log_file (str, optional): Path to the log file. Defaults to None.
            level (int, optional): Logging level. Defaults to logging.INFO.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Remove existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # Add console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Add file handler if log_file is provided
        if log_file:
            self.set_log_file(log_file)

    def set_log_file(self, log_file: str) -> None:
        """Set log file.

        Args:
            log_file (str): Path to the log file.
        """
        if log_file == "default":
            # Save log file in user's home directory with a timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            user_home = os.path.expanduser("~")
            self.log_file = os.path.join(user_home, f"openconv-core_{timestamp}.log")
        else:
            # Use the provided log file path
            self.log_file = os.path.expanduser(log_file)

        file_handler = logging.FileHandler(self.log_file)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def set_log_level(self, level: int) -> None:
        """Set log level.

        Args:
            level (int): Logging level.
        """
        self.log_level = level
        if self.logger:
            self.logger.setLevel(level)


# Create an instance of LoggerConfig
logger_config: LoggerConfig = LoggerConfig()

# Set up logger with default log file location and level
logger_config.setup_logger("openconv-core", log_file="default", level=logging.DEBUG)

# Define the logger to log messages
logger: logging.Logger = logger_config.logger
