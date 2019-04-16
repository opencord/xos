import json
import os
import sys
from backuphandler import BackupHandler

from xosconfig import Config
from multistructlog import create_logger

if __name__ == "__main__":
    Config.init()

log = create_logger(Config().get("logging"))


class BackupProcessor(object):
    def __init__(self):
        self.backup_request_dir = "/var/run/xos/backup/requests"
        self.backup_response_dir = "/var/run/xos/backup/responses"
        self.backup_file_dir = "/var/run/xos/backup/local"

    def build_response_from_request(self, req):
        resp = {"id": req["id"]}
        return resp

    def finalize_response(self, request, response, status):
        log.info("Finalizing response", status=status)
        response["status"] = status
        fn = os.path.join(self.backup_response_dir, request["request_fn"] + "_response")
        open(fn, "w").write(json.dumps(response))
        os.remove(request["request_pathname"])
        return status

    def handle_backup_request(self, req):
        resp = self.build_response_from_request(req)

        if not req.get("backend_filename"):
            if not os.path.exists(self.backup_file_dir):
                os.makedirs(self.backup_file_dir)
            req["backend_filename"] = os.path.join(self.backup_file_dir, "the_backup")

        try:
            BackupHandler.backup(req["backend_filename"])
        except Exception as e:
            log.exception("Backup failed")
            return self.finalize_response(req, resp, "failure")

        log.info("Backup successful")
        resp["backend_filename"] = req["backend_filename"]
        return self.finalize_response(req, resp, "success")

    def handle_restore_request(self, req):
        resp = self.build_response_from_request(req)

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
        BackupHandler.backup(emergency_rollback_fn)

        # TODO: Empty the database

        # TODO: Perform a django loaddata

        log.info("Restore successful")
        resp["status"] = "restored"
        self.save_response(req["request_fn"], resp)
        os.remove(req["request_pathname"])
    
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
