
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
import event_loop
import backend

class TestControllerDependencies(unittest.TestCase):
    def setUp(self):
        b = backend.Backend()
        steps_dir = Config.get("steps_dir")
        self.steps = b.load_sync_step_modules(steps_dir)
        self.synchronizer = event_loop.XOSObserver(self.steps)

    def test_controller_path_simple(self):
        p = Instance()
        s = Slice()
        t = Site()
        ct = ControllerSite()
        p.slice = s
        s.site = t
        ct.site = t
        cohorts = self.synchronizer.compute_dependent_cohorts([p,ct], False)
        self.assertEqual([p, ct], cohorts[0])
        cohorts = self.synchronizer.compute_dependent_cohorts([ct,p], False)
        self.assertEqual([p, ct], cohorts[0])

    def test_controller_deletion_path(self):
        p = Instance()
        s = Slice()
        t = Site()
        ct = ControllerSite()
        ct.site = t
        p.slice = s
        s.site = t
        import pdb
        pdb.set_trace()
        cohorts = self.synchronizer.compute_dependent_cohorts([p,s,t,ct], False)
        cohorts = self.synchronizer.compute_dependent_cohorts([p,s,t,ct], True)


if __name__ == '__main__':
    unittest.main()
