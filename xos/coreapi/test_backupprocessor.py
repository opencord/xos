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

import functools
import json
import os
import pdb
import sys
import unittest
from mock import MagicMock, Mock, patch, ANY
from pyfakefs import fake_filesystem_unittest
from io import open

# pyfakefs breaks these
from __builtin__ import dir as builtin_dir

from xosconfig import Config

class TestBackupProcessor(fake_filesystem_unittest.TestCase):
    def setUp(self):
        config = os.path.abspath(
            os.path.dirname(os.path.realpath(__file__)) + "/test_config.yaml"
        )
        Config.clear()  # in case left unclean by a previous test case
        Config.init(config)

        import backupprocessor
        self.backupprocessor = backupprocessor

        self.setUpPyfakefs()

        self.processor = backupprocessor.BackupProcessor()
        self.mock_backuphandler = MagicMock(backup = MagicMock(), restore=MagicMock())

    def tearDown(self):
        pass

    def test_compute_checksum(self):
        with open("/tmp/somefile", "w") as somefile:
            somefile.write("test")
            self.assertEqual(self.processor.compute_checksum("/tmp/somefile"), 
                             "sha1:da39a3ee5e6b4b0d3255bfef95601890afd80709")

    def test_try_models(self):
        with patch("os.system") as os_system:
            os_system.return_value = 0
            self.processor.try_models()

            os_system.assert_called_with("python try_models.py")

    def test_emergency_rollback(self):
        with patch.object(self.processor, "get_backuphandler") as get_backuphandler:
            get_backuphandler.return_value = self.mock_backuphandler

            self.processor.emergency_rollback("/tmp/foo")
            self.mock_backuphandler.restore.assert_called_with("/tmp/foo")

    def test_finalize_response(self):
        os.makedirs(self.processor.backup_request_dir)
        os.makedirs(self.processor.backup_response_dir)

        request_fn = "request"
        request_pathname = os.path.join(self.processor.backup_request_dir, request_fn)
        response_fn = os.path.join(self.processor.backup_response_dir, "request_response")
        file_details = {"id": 7,
                        "name": "mybackup",
                        "uri": "file:///mybackup",
                        "backend_filename": "/mybackup"}
        req = {"id": 3,
               "operation": "create",
               "file_details": file_details,
               "request_fn": request_fn,
               "request_pathname": request_pathname}

        with open(request_pathname, "w") as req_fn:
            req_fn.write(json.dumps(req))

        resp = {}

        self.processor.finalize_response(req, resp, "created", checksum="1234")

        self.assertTrue(os.path.exists(response_fn))
        data = json.loads(open(response_fn).read())

        expected_data = {u'status': u'created', 
                         u'effective_date': ANY,
                         u'operation': u'create', 
                         u'id': 3, 
                         u'file_details': {u'backend_filename': 
                                           u'/mybackup', 
                                           u'checksum': u'1234', 
                                           u'uri': u'file:///mybackup', 
                                           u'name': u'mybackup', 
                                           u'id': 7}}
        self.assertDictEqual(data, expected_data)
        


def main():
    unittest.main()


if __name__ == "__main__":
    main()
