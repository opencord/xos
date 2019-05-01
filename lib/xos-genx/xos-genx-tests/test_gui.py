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

from __future__ import absolute_import
import unittest
from xosgenx.generator import XOSProcessor, XOSProcessorArgs
from helpers import XProtoTestHelpers


class XProtoGuiTest(unittest.TestCase):
    def setUp(self):
        self.target = XProtoTestHelpers.write_tmp_target(
            """
            {%- for m in proto.messages %}
            {% for f in m.fields %}
                {{ xproto_validators(f) }}
            {% endfor -%}
            {% endfor -%}
            """
        )

    def test_tosca_fields(self):
        """
        [XOS-GenX] should convert xproto types to tosca know types
        """
        xproto = """
        option app_label = "test";

        message Foo {
            required string name = 1 [max_length = 200];
        }
        """

        args = XOSProcessorArgs()
        args.inputs = xproto
        args.target = self.target
        output = XOSProcessor.process(args)
        self.assertIn("{'int_value': 200, 'name': 'maxlength'}", output)
        self.assertIn("{'bool_value': True, 'name': 'required'}", output)

if __name__ == "__main__":
    unittest.main()