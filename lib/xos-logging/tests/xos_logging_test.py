import unittest
from xoslogging import Logger
import logging
import logging.config
import logging.handlers
import structlog
from mock import patch



class XOSLoggingTest(unittest.TestCase):

    def test_get_logging_level(self):
        """ 
        [XOS-Logging] Should return logging level.
        """
        res = Logger.get_logging_level("info")
        self.assertEquals(res, logging.INFO)

        res = Logger.get_logging_level("CRITICAL")
        self.assertEquals(res, logging.CRITICAL)

        res = Logger.get_logging_level("Test")
        self.assertEquals(res, logging.INFO)

    def test_configure_console_logger(self):
        """ 
        [XOS-Logging] Should configure the console logger.
        """
        res = Logger.configure_console_logger(logging.INFO, '%(message)s')

        consoleLogger = logging.getLogger("xos-logger")
        consoleLogger.setLevel(logging.INFO)
        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(logging.INFO)
        streamHandler.setFormatter('%(message)s')
        consoleLogger.addHandler(streamHandler)
        consoleLogger.propagate = False

        self.assertEquals(res, consoleLogger)

    def test_configure_root_logger(self):
        """ 
        [XOS-Logging] Should configure the root logger.
        """
        Logger.set_file_configuration(logging.INFO, 'var//log//xos-core.log')

        res = Logger.configure_root_logger(logging.INFO)

        sample_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {'terse': {'format': '%(message)s'}},
            'handlers': {'file': {'backupCount': '5', 'level': 20, \
                                  'filename': 'var//log//xos-core.log', \
                                  'formatter': 'terse', \
                                  'class': 'logging.handlers.RotatingFileHandler', \
                                  'maxBytes': '1000000'}},
            'loggers': {},
            'root': {
                'handlers': ['file'],
                'level': 20,
            }
        }

        logging.config.dictConfig(sample_config)

        self.assertEquals(res, logging.getLogger())


    def test_configure_struct_logger(self):
        """
        [XOS-GenX] Should configure struct logger.
        """
        with patch('structlog.configure') as sl:
            Logger.configure_struct_logger()
            sl.assert_called_once()
            args = sl.call_args
            self.assertTrue('processors' in args[1])
            self.assertTrue('wrapper_class' in args[1])
            self.assertTrue('context_class' in args[1])
            self.assertTrue('logger_factory' in args[1])

