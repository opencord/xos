#!/usr/bin/env python

# ----------------------------------------------------------------------
# Copyright (c) 2008 Board of Trustees, Princeton University
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and/or hardware specification (the "Work") to
# deal in the Work without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Work, and to permit persons to whom the Work
# is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Work.
#
# THE WORK IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE WORK OR THE USE OR OTHER DEALINGS
# IN THE WORK.
# ----------------------------------------------------------------------

import logging
import logging.config
import logging.handlers
import structlog
from xosconfig import Config
import default

CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG

SAMPLE_CONF = "/Users/shivanivaidya/Desktop/cord/orchestration/xos/lib/xos-config/tests/confs/sample_conf.yaml"

structLogger = structlog.get_logger("structured-xos-logger")
consoleLogger = logging.getLogger("xos-logger")

handlers = []
handlerConfig = {}
formatters = {}


class Logger:
    @staticmethod
    def init():

        Config.init(SAMPLE_CONF)

        channels = Config.get("logging.channels")
        level_str = Config.get("logging.level")

        level = Logger.get_logging_level(level_str)

        if ("console" in channels):
            format = logging.Formatter(default.console_format_str)
            Logger.configure_console_logger(level, format)

        if ("file" in channels):
            name = Config.get("name")
            logfile_path = 'var//log//' + name + '.log'
            Logger.set_file_configuration(level, logfile_path)

        Logger.configure_root_logger(level)

        Logger.configure_struct_logger()

    # allow config-file override of console/logfile level
    @staticmethod
    def get_logging_level(level_str):
        level_str = level_str.lower()

        if level_str == "info":
            return INFO
        elif level_str == "debug":
            return DEBUG
        elif level_str == "warning":
            return WARNING
        elif level_str == "error":
            return ERROR
        elif level_str == "critical":
            return CRITICAL
        else:
            logging.info("Invalid level found in the config file. Setting level to INFO.")
            return INFO

    @staticmethod
    def configure_console_logger(level, format):
        consoleLogger.setLevel(level)
        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(level)
        streamHandler.setFormatter(format)
        consoleLogger.addHandler(streamHandler)
        consoleLogger.propagate = False
        return consoleLogger

    @staticmethod
    def set_file_configuration(level, logfile_path):
        file_config = {
            'level': level,
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': '1000000',
            'backupCount': '5',
            'filename': logfile_path,
            'formatter': 'terse'
        }
        handlers.append('file')
        handlerConfig['file'] = file_config
        terse = {'format': default.terse_format}
        formatters['terse'] = terse

    @staticmethod
    def configure_root_logger(level):
        root_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': formatters,
            'handlers': handlerConfig,
            'loggers': {},
            'root': {
                'handlers': handlers,
                'level': level,
            }
        }
        logging.config.dictConfig(root_config)
        return logging.getLogger()

    @staticmethod
    def configure_struct_logger():
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_log_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeEncoder(),
                structlog.processors.KeyValueRenderer(
                    key_order=[],
                ),
            ],
            wrapper_class=None,
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
        )

if __name__ == '__main__':
    logger = Logger()
    logger.init()
    structLogger.info('user did something', something='shot_in_foot')
    consoleLogger.info('user did something')