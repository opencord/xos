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


class TestModelPolicyTestserviceServiceInstance(unittest.TestCase):

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
        from model_policy_testservice_serviceinstance import TestserviceServiceInstancePolicy
        # import all class names to globals
        for (k, v) in model_accessor.all_model_classes.items():
            globals()[k] = v

        # Some of the functions we call have side-effects, reset the world.
        model_accessor.reset_all_object_stores()

        self.policy = TestserviceServiceInstancePolicy()
        self.si = Mock()

    def tearDown(self):
        sys.path = self.sys_path_save
        self.si = None

    def test_not_synced(self):
        self.si.valid = "awaiting"
        self.si.backend_code = 0

        with self.assertRaises(Exception) as e:
            self.policy.handle_update(self.si)

        self.assertIn("has not been synced yet", e.exception.message)

    def test_skip_update(self):
        self.si.valid = "awaiting"
        self.si.backend_code = 1

        self.policy.handle_update(self.si)


if __name__ == '__main__':
    unittest.main()
