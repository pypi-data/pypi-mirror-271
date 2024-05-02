import pytest
import os

from unittest.mock import patch
from mqtt_middlware_utils import logging_utils as utils


class TestLoggingUtils:

    test_log_file = "tests/files/test_log.log"

    def clear_log_file(self):
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)

    def read_file_line(self):
        if os.path.exists(self.test_log_file):
            with open(self.test_log_file, "r") as f:
                return f.readline()

    def test_map_log_level_debug(self):
        log_level_string = "DEBUG"
        mapped_log_level = utils.map_log_level(log_level_string)
        assert mapped_log_level == utils.logging.DEBUG

    def test_map_log_level_info(self):
        log_level_string = "INFO"
        mapped_log_level = utils.map_log_level(log_level_string)
        assert mapped_log_level == utils.logging.INFO

    def test_map_log_level_warning(self):
        log_level_string = "WARNING"
        mapped_log_level = utils.map_log_level(log_level_string)
        assert mapped_log_level == utils.logging.WARNING

    def test_map_log_level_error(self):
        log_level_string = "ERROR"
        mapped_log_level = utils.map_log_level(log_level_string)
        assert mapped_log_level == utils.logging.ERROR

    def test_map_log_level_undefined_log_level(self):
        log_level_string = "WRONG_LEVEL"
        mapped_log_level = utils.map_log_level(log_level_string)
        assert mapped_log_level == utils.logging.INFO

    def test_init_logger(self):
        log_level = "WARNING"
        logger_name = "test_logger"
        log_destination = "tests/files/test_log.log"
        initialized_logger = utils.init_logger(
            log_level, logger_name, log_destination)

        assert initialized_logger.level == utils.logging.WARNING
        assert initialized_logger.name == logger_name
        assert len(initialized_logger.handlers) != 0

    def test_init_logger_exception_raise(self):
        with patch('mqtt_middlware_utils.logging_utils.init_logger',
                   side_effect=utils.LoggerInitException("Error initializing logger")):
            with pytest.raises(utils.LoggerInitException):
                utils.init_logger("LOG_LEVEL", "LOGGER_NAME",
                                  "LOG_DESTINATION")

    def test_log_info(self):
        log_level = "DEBUG"
        msg = "JUST A TEST FOR INFO LOGGING"
        logger_name = "test_logger"

        # delete log file if it exists
        self.clear_log_file()

        logger = utils.init_logger(
            log_level, logger_name, self.test_log_file)
        utils.log_info(logger_name, msg)
        written_line = self.read_file_line()

        assert "INFO" in written_line
        assert msg in written_line

    def test_log_info_exception_raise(self):
        with patch('mqtt_middlware_utils.logging_utils.log_info',
                   side_effect=utils.LoggerException("Error with logging info")):
            with pytest.raises(utils.LoggerException):
                log_level = "INFO"
                msg = "JUST A TEST MESSAGE"
                logger_name = "test_logger"

                self.clear_log_file()
                logger = utils.init_logger(
                    log_level, logger_name, self.test_log_file)
                utils.log_info(logger_name, msg)

    def test_log_debug(self):
        log_level = "DEBUG"
        msg = "JUST A TEST FOR DEBUG LOGGING"
        logger_name = "test_logger"

        # delete log file if it exists
        self.clear_log_file()

        logger = utils.init_logger(
            log_level, logger_name, self.test_log_file)
        utils.log_debug(logger_name, msg)
        written_line = self.read_file_line()

        assert "DEBUG" in written_line
        assert msg in written_line

    def test_log_debug_exception_raise(self):
        with patch('mqtt_middlware_utils.logging_utils.log_debug',
                   side_effect=utils.LoggerException("Error with logging debug")):
            with pytest.raises(utils.LoggerException):
                log_level = "DEBUG"
                msg = "JUST A TEST FOR DEBUG LOGGING"
                logger_name = "test_logger"

                self.clear_log_file()
                logger = utils.init_logger(
                    log_level, logger_name, self.test_log_file)
                utils.log_debug(logger_name, msg)

    def test_log_error(self):
        log_level = "DEBUG"
        msg = "JUST A TEST FOR ERROR LOGGING"
        logger_name = "test_logger"

        # delete log file if it exists
        self.clear_log_file()

        logger = utils.init_logger(
            log_level, logger_name, self.test_log_file)
        utils.log_error(logger_name, msg)
        written_line = self.read_file_line()

        assert "ERROR" in written_line
        assert msg in written_line

    def test_log_error_exception_raise(self):
        with patch('mqtt_middlware_utils.logging_utils.log_error',
                   side_effect=utils.LoggerException("Error with logging error")):
            with pytest.raises(utils.LoggerException):
                log_level = "DEBUG"
                msg = "JUST A TEST FOR ERROR LOGGING"
                logger_name = "test_logger"

                self.clear_log_file()
                logger = utils.init_logger(
                    log_level, logger_name, self.test_log_file)
                utils.log_error(logger_name, msg)

    def test_log_warning(self):
        log_level = "DEBUG"
        msg = "JUST A TEST FOR WARNING LOGGING"
        logger_name = "test_logger"

        # delete log file if it exists
        self.clear_log_file()

        logger = utils.init_logger(
            log_level, logger_name, self.test_log_file)
        utils.log_warning(logger_name, msg)
        written_line = self.read_file_line()

        assert "WARNING" in written_line
        assert msg in written_line

    def test_log_warning_exception_raise(self):
        with patch('mqtt_middlware_utils.logging_utils.log_warning',
                   side_effect=utils.LoggerException("Error with logging warning")):
            with pytest.raises(utils.LoggerException):
                log_level = "DEBUG"
                msg = "JUST A TEST FOR WARNING LOGGING"
                logger_name = "test_logger"

                self.clear_log_file()
                logger = utils.init_logger(
                    log_level, logger_name, self.test_log_file)
                utils.log_warning(logger_name, msg)
