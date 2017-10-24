import logging
import os

from nose2.events import Plugin

log = logging.getLogger('nose2.plugins.excludeignoredfiles')

class ExcludeIgnoredFiles(Plugin):
    commandLineSwitch = (None, 'exclude-ignored-files', 'Exclude that which should be excluded')

    def matchPath(self, event):
        if event.path.endswith(".py"):
            text = open(event.path, "r").read()
            if "test_framework: ignore" in text.lower():
                log.info("Ignoring %s" % event.path)
                event.handled = True
                return False
