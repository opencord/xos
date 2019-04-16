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
        response["file_details"] = request.get("file_details", {})

        fn = os.path.join(self.backup_response_dir, request["request_fn"] + "_response")
        open(fn, "w").write(json.dumps(response))
        os.remove(request["request_pathname"])
        return status

    def handle_backup_request(self, req):
        resp = {}

        if not req.get("backend_filename"):
            if not os.path.exists(self.backup_file_dir):
                os.makedirs(self.backup_file_dir)
            req["backend_filename"] = os.path.join(self.backup_file_dir, "the_backup")

        try:
            BackupHandler().backup(req["backend_filename"])
        except Exception as e:
            log.exception("Backup failed")
            return self.finalize_response(req, resp, "failure")

        log.info("Backup successful")
        resp["backend_filename"] = req["backend_filename"]
        return self.finalize_response(req, resp, "created")

    def handle_restore_request(self, req):
        resp = {}

        backend_filename = req.get("backend_filename")
        if not backend_filename:
            log.error("request is missing backend_filename", req)
            return self.finalize_response(req, resp, "failure")

        if not os.path.exists(backend_filename):
            log.error("restore file does not exist", backend_filename)
            return self.finalize_response(req, resp, "failure")

        # Step 1: Perform the emergency-rollback backup

        if not os.path.exists(self.backup_file_dir):
            os.makedirs(self.backup_file_dir)

        emergency_rollback_fn = os.path.join(self.backup_file_dir, "emergency_rollback")
        BackupHandler().backup(emergency_rollback_fn)

        try:
            BackupHandler().restore(backend_filename)
        except:
            log.exception("Exception while performing database restore")
            BackupHandler().restore(emergency_rollback_fn)
            log.exception("Performing emergency rollback")
            return self.finalize_response(req, resp, "failure")

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
                # If we can't read it then ignore and delete it
                log.exception("Failed to read backup request", fn=pathname)
                continue

            try:
                id = contents["id"]
                operation = contents["operation"]
            except Exception:
                # If we can't understand it then ignore and delete it
                log.exception("Failed to understand backup request", fn=pathname)
                continue

            log.info("Processing request", id=id, operation=operation)

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
