from unittest import TestCase

from app.logger import Logger

CRITICAL_MSG = "CRITICAL log!"
DEBUG_MSG = "DEBUG log!"
ERROR_MSG = "ERROR log!"
INFO_MSG = "INFO log!"
WARNING_MSG = "WARNING log!"

logger = None


class TestLogger(TestCase):

    def get_log_output(self, log_level):
        with self.assertLogs() as log_output:
            global logger
            logger = Logger(__name__).set_logger(log_level)
            logger.critical(CRITICAL_MSG)
            logger.debug(DEBUG_MSG)
            logger.error(ERROR_MSG)
            logger.info(INFO_MSG)
            logger.warning(WARNING_MSG)
        return log_output

    def test_logger_default(self):
        logged = self.get_log_output(None)
        self.assertEqual(4, len(logged.records))
        self.assertEqual("{} log!".format('CRITICAL'), logged.records[0].getMessage())
        self.assertEqual("{} log!".format('ERROR'), logged.records[1].getMessage())
        self.assertEqual("{} log!".format('INFO'), logged.records[2].getMessage())
        self.assertEqual("{} log!".format('WARNING'), logged.records[3].getMessage())

    def test_logger_critical(self):
        level = 'CRITICAL'
        logged = self.get_log_output(level)
        self.assertEqual(1, len(logged.records))
        self.assertEqual("{} log!".format(level), logged.records[0].getMessage())

    def test_logger_debug(self):
        level = 'DEBUG'
        logged = self.get_log_output(level)
        self.assertEqual(5, len(logged.records))
        self.assertEqual("{} log!".format('CRITICAL'), logged.records[0].getMessage())
        self.assertEqual("{} log!".format(level), logged.records[1].getMessage())
        self.assertEqual("{} log!".format('ERROR'), logged.records[2].getMessage())
        self.assertEqual("{} log!".format('INFO'), logged.records[3].getMessage())
        self.assertEqual("{} log!".format('WARNING'), logged.records[4].getMessage())

    def test_logger_error(self):
        level = 'ERROR'
        logged = self.get_log_output(level)
        self.assertEqual(2, len(logged.records))
        self.assertEqual("{} log!".format('CRITICAL'), logged.records[0].getMessage())
        self.assertEqual("{} log!".format(level), logged.records[1].getMessage())

    def test_logger_info(self):
        level = 'INFO'
        logged = self.get_log_output(level)
        self.assertEqual(4, len(logged.records))
        self.assertEqual("{} log!".format('CRITICAL'), logged.records[0].getMessage())
        self.assertEqual("{} log!".format('ERROR'), logged.records[1].getMessage())
        self.assertEqual("{} log!".format(level), logged.records[2].getMessage())
        self.assertEqual("{} log!".format('WARNING'), logged.records[3].getMessage())

    def test_logger_warning(self):
        level = 'WARNING'
        logged = self.get_log_output(level)
        self.assertEqual(3, len(logged.records))
        self.assertEqual("{} log!".format('CRITICAL'), logged.records[0].getMessage())
        self.assertEqual("{} log!".format('ERROR'), logged.records[1].getMessage())
        self.assertEqual("{} log!".format(level), logged.records[2].getMessage())