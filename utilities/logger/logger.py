# coding: utf-8​
import logging
import logging.handlers
import os
import sys
import time

from utilities.datetime import NeDateTime
from utilities.filesystem import fs
from utilities.strings import NeStrings

curr_environment = os.environ.get('ENVIRONMENT')
if not curr_environment:
    curr_environment = 'DEV'

MSG_FORMAT = '[%(asctime)s.%(msecs)03dZ] [%(levelname)s] [%(app_name)s] [%(app_code)s] [TINAA_BSAF] [%(module)s:%(lineno)d] %(message)s'
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'


class NeLogger:
    skip_file_logs = False

    def __init__(self):
        self.__logger_name = None
        self.__filename = None
        self.__filepath = None
        self.__log_level = logging.INFO
        self.__formatter = logging.Formatter(fmt=MSG_FORMAT, datefmt=DATE_FORMAT)
        self.__formatter.converter = time.localtime

    def name(self, val: str):
        self.__logger_name = val
        return self

    def fileName(self, val: str):
        self.__filename = val
        return self

    def filePath(self, val: str):
        self.__filepath = val
        return self

    def level(self, val: str):
        self.__log_level = val
        return self

    def getRootLogger(self):
        lgr = logging.getLogger(self.__logger_name)
        lgr.setLevel(self.__log_level or logging.INFO)
        filename_with_path = self.__getFileNameWithPath(filename=self.__filename)
        # Define the formatter
        if not len(lgr.handlers):
            if not curr_environment or curr_environment != "local":
                lgr.addHandler(self.__getFileHandler(filename_with_path))
            #
            stderr_handler = logging.StreamHandler(sys.stderr)
            stderr_handler.setFormatter(self.__formatter)
            lgr.addHandler(stderr_handler)
        lgr.propagate = False  # prevent getting duplicate messages from root logger (lgr)
        format_conf = {
            'app_code': '0000',
            'app_name': self.__logger_name
        }
        logger_obj = logging.LoggerAdapter(lgr, format_conf)
        return logger_obj

    def __getFileNameWithPath(self, filename: str = None, location: str = None) -> str:
        # Define the location of the log file, if no directory then create new directory
        if location is None:
            import nest_globals
            location = os.path.join(nest_globals.ROOT_DIR, "logs/")
        if not os.path.exists(location):
            os.makedirs(location)
        filename = NeStrings.defaultIfEmpty(filename, f'log_{NeDateTime.yyyymmddhhmmss()}')
        filename = f'{filename}.log'
        filename_with_path = location + filename
        return filename_with_path

    def __getFileHandler(self, filename_with_path: str):
        file_handler = logging.handlers.TimedRotatingFileHandler(filename_with_path,
                                                                 when='midnight',
                                                                 interval=1,
                                                                 backupCount=7,
                                                                 utc=False)
        file_handler.setFormatter(self.__formatter)
        return file_handler

    def attachLogHandler(self, filename: str, filepath: str, log_level=logging.INFO):
        if not fs.exists(filepath):
            fs.createDirectory(filepath)
        full_file_path = os.path.abspath(os.path.join(filepath, filename))
        fh = self.__getFileHandler(full_file_path)
        fh.setLevel(log_level or logging.DEBUG)
        logger.logger.addHandler(fh)
        return fh

    def detachLogHandler(self, fh):
        logger.logger.removeHandler(fh)

# logger = NeLogger.getNestLogger('nest-test-engine', log_level=logging.DEBUG)
logger = NeLogger().name('nest-test-engine').fileName('nest-work-engine').level(logging.DEBUG).getRootLogger()
