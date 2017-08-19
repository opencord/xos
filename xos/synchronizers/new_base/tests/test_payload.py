
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


import unittest
from mock import patch
import mock
import pdb
import networkx as nx

import os, sys

sys.path.append("../..")
sys.path.append("../../new_base")
config =  os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/test_config.yaml")
from xosconfig import Config
Config.init(config, 'synchronizer-config-schema.yaml')

import synchronizers.new_base.modelaccessor
from steps.mock_modelaccessor import *
import mock
import event_loop
import backend
import json

import steps.sync_instances

ANSIBLE_FILE='/tmp/payload_test'

def run_fake_ansible_template(*args,**kwargs):
    opts = args[1]
    open(ANSIBLE_FILE,'w').write(json.dumps(opts))

def get_ansible_output():
    ansible_str = open(ANSIBLE_FILE).read()
    return json.loads(ansible_str)

class TestPayload(unittest.TestCase):
    def setUp(self):
        b = backend.Backend()
        steps_dir = Config.get("steps_dir")
        self.steps = b.load_sync_step_modules(steps_dir)
        self.synchronizer = event_loop.XOSObserver(self.steps)

    @mock.patch("steps.sync_instances.syncstep.run_template",side_effect=run_fake_ansible_template)
    @mock.patch("event_loop.model_accessor")
    def test_delete_record(self, mock_run_template, mock_modelaccessor):
        o = Instance()
        o.name = "Sisi Pascal"

        o.synchronizer_step = steps.sync_instances.SyncInstances()
        self.synchronizer.delete_record(o)

        a = get_ansible_output()
        self.assertDictContainsSubset({'delete':True, 'name':o.name}, a)
        
    @mock.patch("steps.sync_instances.syncstep.run_template",side_effect=run_fake_ansible_template)
    @mock.patch("event_loop.model_accessor")
    def test_sync_record(self, mock_run_template, mock_modelaccessor):
        o = Instance()
        o.name = "Sisi Pascal"

        o.synchronizer_step = steps.sync_instances.SyncInstances()
        self.synchronizer.sync_record(o)

        a = get_ansible_output()
        self.assertDictContainsSubset({'delete':False, 'name':o.name}, a)
if __name__ == '__main__':
    unittest.main()
