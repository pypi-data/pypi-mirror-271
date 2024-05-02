import logging

from logging.handlers import TimedRotatingFileHandler
from mqtt_middlware_utils.exceptions.mqtt_middleware_exceptions import LoggerInitException, LoggerException


def map_log_level(log_level_string):
    '''
    Maps the provided string to a logging level. 
    If the provided string can't be mapped to a valid logging level, 
    the default level INFO is selected.

    @param log_level_string string to map to

    @return mapped logging level
    '''
    mapped_log_level = logging.INFO
    if log_level_string == "DEBUG":
        mapped_log_level = logging.DEBUG
    if log_level_string == "ERROR":
        mapped_log_level = logging.ERROR
    if log_level_string == "WARNING":
        mapped_log_level = logging.WARNING

    return mapped_log_level


def init_logger(log_level, logger_name, log_destination):
    '''
    Initialize a logger with the provided logger_name.

    @param log_level logging level of the logger
    @param logger_name name of the logger
    @param log_destination path to the log file

    @return the initialized logger instance

    @raise LoggerInitException if an error occurs while initializing the logger

    '''
    try:
        # create custom logger
        logger = logging.getLogger(logger_name)
        # set logging level
        logger.setLevel(map_log_level(log_level))
        # create handler
        # TimedRotatingFileHandler handles log files rotating based on time
        handler = TimedRotatingFileHandler(
            log_destination, "D", utc=True, backupCount=30)
        # set format for logging
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    except Exception as e:
        raise LoggerInitException(
            "The following error occurred while initializing the logger: " + str(e))


def log_info(logger_name, msg):
    '''
    Logs the provided message as INFO.

    @param logger_name name of the logger
    @param msg the message to be logged

    @raise LoggerException if an error occurs while logging info

    '''
    try:
        logging.getLogger(logger_name).info(msg)
    except Exception as e:
        raise LoggerException(
            "The following error occurred while logging info: " + str(e))


def log_debug(logger_name, msg):
    '''
    Logs the provided message as DEBUG.

    @param logger_name name of the logger
    @param msg the message to be logged

    @raise LoggerException if an error occurs while logging debug

    '''
    try:
        logging.getLogger(logger_name).debug(msg)
    except Exception as e:
        raise LoggerException(
            "The following error occurred while logging debug: " + str(e))


def log_error(logger_name, msg):
    '''
    Logs the provided message as ERROR.

    @param logger_name name of the logger
    @param msg the message to be logged

    @raise LoggerException if an error occurs while logging error

    '''
    try:
        logging.getLogger(logger_name).error(msg)
    except Exception as e:
        raise LoggerException(
            "The following error occurred while logging error: " + str(e))


def log_warning(logger_name, msg):
    '''
    Logs the provided message as WARNING.

    @param logger_name name of the logger
    @param msg the message to be logged

    @raise LoggerException if an error occurs while logging warning
    '''
    try:
        logging.getLogger(logger_name).warning(msg)
    except Exception as e:
        raise LoggerException(
            "The following error occurred while logging warning: " + str(e))
