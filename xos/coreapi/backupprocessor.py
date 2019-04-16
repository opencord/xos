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

""" BackupProcessor

    This runs after the core process has completed, and is responsible for performing the actual
    backup and restore operations. Requests are read from a local directory, acted upon, and
    responses are written out to another directory.
"""

import json
import os
import sys

from xosconfig import Config
from multistructlog import create_logger

if __name__ == "__main__":
    Config.init()

# Must be after config.init()
from backuphandler import BackupHandler

log = create_logger(Config().get("logging"))


class BackupProcessor(object):
    def __init__(self):
        self.backup_request_dir = "/var/run/xos/backup/requests"
        self.backup_response_dir = "/var/run/xos/backup/responses"
        self.backup_file_dir = "/var/run/xos/backup/local"

    def finalize_response(self, request, response, status):
        log.info("Finalizing response", status=status, id=request["id"])
        response["id"] = request["id"]
        response["status"] = status
        response["operation"] = request["operation"]
        response["file_details"] = request["file_details"]

        fn = os.path.join(self.backup_response_dir, request["request_fn"] + "_response")
        open(fn, "w").write(json.dumps(response))
        os.remove(request["request_pathname"])
        return status

    def handle_backup_request(self, req):
        resp = {}

        backend_filename = req["file_details"]["backend_filename"]
        backend_filename_dir = os.path.dirname(backend_filename)
        if not backend_filename_dir:
            log.error("backend_filename should include a directory", req)
            return self.finalize_response(req, resp, "failure")

        # Ensure the backup directory exists
        if not os.path.exists(backend_filename_dir):
            os.makedirs(backend_filename_dir)

        try:
            BackupHandler().backup(backend_filename)
        except Exception:
            log.exception("Backup failed")
            return self.finalize_response(req, resp, "failure")

        log.info("Backup successful")
        return self.finalize_response(req, resp, "created")

    def handle_restore_request(self, req):
        resp = {}

        backend_filename = req["file_details"]["backend_filename"]
        if not os.path.exists(backend_filename):
            log.error("restore file does not exist", backend_filename)
            return self.finalize_response(req, resp, "failure")

        # Step 1: Perform the emergency-rollback backup

        if not os.path.exists(self.backup_file_dir):
            os.makedirs(self.backup_file_dir)

        emergency_rollback_fn = os.path.join(self.backup_file_dir, "emergency_rollback")

        try:
            BackupHandler().backup(emergency_rollback_fn)
        except Exception:
            log.exception("Exception while creating emergency rollback file")
            return self.finalize_response(req, resp, "failure")

        # Step 2: Perform the restore

        try:
            BackupHandler().restore(backend_filename)
        except Exception:
            log.exception("Exception while performing database restore")
            BackupHandler().restore(emergency_rollback_fn)
            log.info("Performing emergency rollback")
            return self.finalize_response(req, resp, "failure")

        # Step 3: Verify model integrity

        # TODO: try_models and perform rollback as necessary

        log.info("Restore successful")
        return self.finalize_response(req, resp, "restored")
    
    def run(self):
        # make sure the directory exists
        if not os.path.exists(self.backup_request_dir):
            os.makedirs(self.backup_request_dir)

        for fn in os.listdir(self.backup_request_dir):
            pathname = os.path.join(self.backup_request_dir, fn)
            if os.path.isdir(pathname) or pathname.startswith("."):
                continue
            
            try:
                contents = json.loads(open(pathname).read())
            except Exception:
                # If we can't read it then ignore it
                log.exception("Failed to read backup request", fn=pathname)
                continue

            try:
                id = contents["id"]
                operation = contents["operation"]
                backend_filename = contents["file_details"]["backend_filename"]
            except Exception:
                # If we can't understand it then ignore it
                log.exception("Failed to understand backup request", fn=pathname)
                continue
                    
            log.info("Processing request",
                     id=id,
                     operation=operation,
                     backend_filename=backend_filename)

            contents["request_fn"] = fn
            contents["request_pathname"] = pathname

            if (operation == "create"):
                self.handle_backup_request(contents)
            elif (operation == "restore"):
                self.handle_restore_request(contents)
            else:
                log.error("Operation is not create|restore", operation=operation)

if __name__ == "__main__":
    BackupProcessor().run()
