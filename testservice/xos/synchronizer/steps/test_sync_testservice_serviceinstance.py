# Copyright 2018-present Open Networking Foundation
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

import os
import sys
import unittest
from mock import Mock

# Hack to load synchronizer framework
test_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

xos_dir = os.path.join(test_path, "../../..")

if not os.path.exists(os.path.join(test_path, "new_base")):
    xos_dir = os.path.join(test_path, "../../../../../../orchestration/xos/xos")
    services_dir = os.path.join(xos_dir, "../../xos_services")

sys.path.append(xos_dir)
sys.path.append(os.path.join(xos_dir, 'synchronizers', 'new_base'))
# END Hack to load synchronizer framework


# generate model from xproto
def get_models_fn(service_name, xproto_name):
    name = os.path.join(service_name, "xos", xproto_name)
    if os.path.exists(os.path.join(services_dir, name)):
        return name
    else:
        name = os.path.join(service_name, "xos", "synchronizer", "models", xproto_name)
        if os.path.exists(os.path.join(services_dir, name)):
            return name
    raise Exception("Unable to find service=%s xproto=%s" % (service_name, xproto_name))
# END generate model from xproto


class TestSyncTestserviceServiceInstance(unittest.TestCase):

    def setUp(self):

        self.sys_path_save = sys.path
        sys.path.append(xos_dir)
        sys.path.append(os.path.join(xos_dir, 'synchronizers', 'new_base'))

        # Setting up the config module
        from xosconfig import Config
        config = os.path.join(test_path, "../test_config.yaml")
        Config.clear()
        Config.init(config, "synchronizer-config-schema.yaml")
        # END Setting up the config module

        from synchronizers.new_base.mock_modelaccessor_build import build_mock_modelaccessor
        build_mock_modelaccessor(xos_dir, services_dir, [
            get_models_fn("testservice", "testservice.xproto"),
        ])

        from synchronizers.new_base.modelaccessor import model_accessor
        from sync_testservice_serviceinstance import SyncTestserviceServiceInstance
        # import all class names to globals
        for (k, v) in model_accessor.all_model_classes.items():
            globals()[k] = v

        self.sync_step = SyncTestserviceServiceInstance

        # create a mock instance instance
        self.model = Mock()
        self.model.name = "Example"

    def tearDown(self):
        self.model = None
        sys.path = self.sys_path_save

    # TODO - The following two tests are very simple, replace with more meaningful ones

    def test_save(self):
        # Tests that the model can be saved

        self.model.name = "testservice_test"
        self.sync_step().sync_record(self.model)
        self.model.save.assert_called()

    def test_sync_rejected(self):
        # Tests that an empty name raises an exception

        self.model.name = ""
        with self.assertRaises(Exception):
            self.sync_step().sync_record(self.model)


if __name__ == '__main__':
    unittest.main()
