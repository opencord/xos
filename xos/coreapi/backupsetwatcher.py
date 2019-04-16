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

""" Backup Set Watcher

    Watches for backup/restore operations. Stops the core so they can be executed.

    The basic idea is that backup/restore requests are written to a directory, and responses are read from another
    directory. After a request has been written the core will exit. Only one request is written at a time. Responses
    are only read when the thread is started, as it's impossible for a response to show up while the core is
    running.

        1. Operator creates BackupSet in the XOS database
        2. BackupSetWatcher notices new BackupSet, writes to file in /var/run/xos/backup/requests
        3. BackupSetWatcher terminates coreapi
        4. coreapi exits
        5. the root core shell script executes backup, writing response to /var/run/xos/backup/responses
        6. the root core shell script restarts coreapi
        7. BackupSetWatcher notices a new response, and updates the appropriate BackupSet object.
"""

import json
import os
import sys
import traceback
import threading
import time

from xosconfig import Config
from multistructlog import create_logger
log = create_logger(Config().get("logging"))

from core.models.backupset import BackupSet


class BackupSetWatcherThread(threading.Thread):
    daemon = True
    interval = 5

    def __init__(self, server, *args, **kwargs):
        self.terminate_signal = False
        super(BackupSetThread, self).__init__(*args, **kwargs)

        self.server = server
        self.exiting = False
        self.backup_request_dir = "/var/run/xos/backup/requests"
        self.backup_response_dir = "/var/run/xos/backup/responses"
        self.process_response_dir()

    def init_request_dir(self):
        # make sure the directory exists
        if not os.path.exists(self.backup_request_dir):
            os.makedirs(self.backup_request_dir)

        # make sure it is empty
        for fn in os.listdir(self.backup_request_dir):
            fn = os.path.join(self.backup_request_dir, fn)
            if os.path.isdir(fn) or fn.startswith("."):
                continue
            os.remove(fn)

    def process_response_dir(self):
        # make sure the directory exists
        if not os.path.exists(self.backup_request_dir):
            os.makedirs(self.backup_request_dir)

        # process the responses and delete them
        for fn in os.listdir(self.backup_request_dir):
            fn = os.path.join(self.backup_request_dir, fn)
            if os.path.isdir(fn) or fn.startswith(".") or (not fn.endswith(".json")):
                continue
            
            try:
                contents = json.loads(open(fn).read())
            except Exception:
                # If we can't read it then ignore and delete it
                log.exception("Failed to read backup response", fn=fn)
                os.remove(fn)
                continue

            try:
                id = contents["id"]
                filename = contents["filename"]
                status = contents["status"]
            except Exception:
                # If we can't understand it then ignore and delete it
                log.exception("Failed to understand backup response", fn=fn)
                os.remove(fn)
                continue

            backupsets = BackupSet.objects.filter(id=id)
            if not backupsets:
                log.exception("Backup response refers to a backupset that does not exist", fn=fn)
                os.remove(fn)
                continue

            # Note: Try to make sure this doesn't cause `updated` to be set
            backupset = backupsets[0]
            backupset.filename = filename
            backupset.status = status
            backupset.enacted = time.time()
            backupset.save(update_fields=["enacted", "filename", "status"]))

            os.remove(fn)

    def save_request(self):
        # TODO: everything

    def run_once(self):
        # If we're exiting due to a backup request being saved, then return
        if self.exiting:
            return

        backupsets = BackupSet.objects.filter(backend_code__ne = 1)
        for backupset in backupsets:
            if backupset.operation not in [`create`, `restore`]:
                # If it's not a create or restore (perhaps it is "failed") then there is
                # nothing for us to do.
                continue

            # There can only be one request at a time. Ensure the directory is empty.
            self.init_request_dir()
            save_request(backupsets[0])
            self.exiting = True
            self.server.delayed_shutdown(0)

            # Stop iterating the loop. Since we set self.exiting=True, we know the loop will
            # not be called again.
            return

    def run(self):
        while not self.terminate_signal:
            start = time.time()
            try:
                self.run_once()
            except BaseException:
                log.exception("backupset_watcher: Exception in run loop")

            telap = time.time() - start
            if telap < self.interval:
                time.sleep(self.interval - telap)

    def stop(self):
        self.terminate_signal = True
