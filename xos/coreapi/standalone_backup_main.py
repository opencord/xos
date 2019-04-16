# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# NOTE: This file only used for development...

import os
import sys
import threading
import time

xos_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/..")
sys.path.append(xos_path)

from xosconfig import Config
from xoskafka import XOSKafkaProducer
from multistructlog import create_logger

Config.init()
log = create_logger(Config().get("logging"))

# create an single kafka producer connection for the core

XOSKafkaProducer.init()


def init_backupset_watcher(server):
    backupset_watcher = None
    try:
        from backupsetwatcher import BackupSetWatcherThread

        backupset_watcher = BackupSetWatcherThread(server)
        backupset_watcher.start()
    except BaseException:
        log.exception("Failed to initialize backupset watcher")

    return backupset_watcher


class FakeServer(threading.Thread):
    def __init__(self):
        super(FakeServer, self).__init__()
        self.daemon = True
        self.delayed_shutdown_timer = None
        self.exit_event = threading.Event()
        self.init_django()

    def run(self):
        while True:
            time.sleep(1)

    def init_django(self):
        try:
            import django

            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xos.settings")
            django.setup()
            from django.apps import apps

            self.django_apps = apps
            self.django_initialized = True
        except BaseException:
            log.exception("Failed to initialize django")

    def stop_and_exit(self):
        log.info("Stop and Exit")
        self.exit_event.set()

    def delayed_shutdown(self, seconds):
        log.info("Delayed shutdown", seconds=seconds)
        if self.delayed_shutdown_timer:
            self.delayed_shutdown_timer.cancel()
        self.delayed_shutdown_timer = threading.Timer(seconds, self.stop_and_exit)
        self.delayed_shutdown_timer.start()


if __name__ == "__main__":
    server = FakeServer()
    server.start()

    if server.django_initialized:
        backupset_watcher = init_backupset_watcher(server)
    else:
        log.warning("Skipping reaper and backupset_watcher as django is not initialized")
        backupset_watcher = None

    log.info("XOS core entering wait loop")
    _ONE_DAY_IN_SECONDS = 60 * 60 * 24
    try:
        while True:
            if server.exit_event.wait(_ONE_DAY_IN_SECONDS):
                break
    except KeyboardInterrupt:
        log.info("XOS core terminated by keyboard interrupt")

    if backupset_watcher:
        backupset_watcher.stop()
