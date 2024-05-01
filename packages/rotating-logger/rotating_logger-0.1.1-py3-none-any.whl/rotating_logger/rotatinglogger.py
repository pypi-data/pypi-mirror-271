import logging
import logging.handlers
import os
from datetime import datetime
from rotating_logger.singleton import singleton


@singleton
class RotatingLogger(object):
    """
    Logger singleton class implementing the logging mechanism:
        - ``debug()``: log at DEBUG level
        - ``info()``: log at INFO level
        - ``warning()``: log at WARNING level
        - ``error()``: log at ERROR level
        - ``critical()``: log at CRITICAL level
    """
    def __init__(
            self,
            backup_count: int = 30,
            encoding: str = 'utf-8',
    ):
        """
        Constructor
        """
        # Instantiate a logger and set its level to DEBUG
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)
        # Format log messages: YYYY-MM-DD hh:mm:ss,sss - [Level] - Msg
        self._formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
        # Checking if logs folder exists and creating it if not
        log_folder = 'logs'
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        # Creating path to log file: 'YYYY-MM-DD.log'
        log_file = os.path.join(log_folder, datetime.now().strftime('%Y-%m-%d.log'))
        # Checking if logger has handlers and adding one if not
        if not self._logger.hasHandlers():
            # Instantiating rotating file handler
            self._file_handler = logging.handlers.RotatingFileHandler(
                filename=log_file,
                maxBytes=1000000,
                backupCount=backup_count,
                encoding=encoding
            )
            # Adding formatter to file handler, and adding file handler to logger
            self._file_handler.setFormatter(self._formatter)
            self._logger.addHandler(self._file_handler)

    def __repr__(self):
        """
        String representation of the logger.
        """
        return self._logger.__repr__() + self._file_handler.__repr__()

    def debug(self, msg):
        """
        Log at the DEBUG level.
        :param msg: the message to log
        """
        self._logger.debug(msg)

    def info(self, msg):
        """
        Log at the INFO level.
        :param msg: the message to log
        """
        self._logger.info(msg)

    def warning(self, msg):
        """
        Log at the WARNING level.
        :param msg: the message to log
        """
        self._logger.warning(msg)

    def error(self, msg):
        """
        Log at the ERROR level.
        :param msg: the message to log
        """
        self._logger.error(msg)

    def critical(self, msg):
        """
        Log at the CRITICAL level.
        :param msg: the message to log
        """
        self._logger.critical(msg)
