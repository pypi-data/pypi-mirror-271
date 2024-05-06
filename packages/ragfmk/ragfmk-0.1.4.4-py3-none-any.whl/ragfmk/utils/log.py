__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

import logging
from logging.handlers import RotatingFileHandler
import ragfmk.utils.CONST as C

class log:
    def __init__(self, 
                 loggerName = C.TRACE_LOGGER, 
                 logfilename = C.TRACE_FILENAME, 
                 level = C.TRACE_DEFAULT_LEVEL, 
                 format = C.TRACE_DEFAULT_FORMAT):
        self.__logger = logging.getLogger(loggerName)
        handler = RotatingFileHandler(logfilename, 
                                         mode="a", 
                                         maxBytes= C.TRACE_MAXBYTES, 
                                         backupCount=10, 
                                         encoding=C.ENCODING)
        handler.setFormatter(logging.Formatter(format))
        self.__logger.setLevel(level)
        self.__logger.addHandler(handler)

    @property
    def logger(self):
        return self.__logger
    
    def display(self, message):
        print(message)
    
    def buildMessage(self, _msg):
        final_message = ""
        for msg in _msg:
            final_message += str(msg)
        return final_message
    
    def info(self, *message):
        final_message = self.buildMessage(message)
        self.display("Info: " + final_message)
        self.logger.info(final_message)

    def error(self, *message):
        final_message = self.buildMessage(message)
        self.display("Error: " + final_message)
        self.logger.error(final_message)

    def debug(self, *message):
        final_message = self.buildMessage(message)
        self.display("Debug: " + final_message)
        self.logger.debug(final_message)

    def warning(self, *message):
        final_message = self.buildMessage(message)
        self.display("Warning: " + final_message)
        self.logger.warning(final_message)