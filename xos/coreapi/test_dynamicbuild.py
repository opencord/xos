
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

import os
import sys
import tempfile
import unittest

from xosconfig import Config

class DynamicBuildItem():
    def __init__(self, **kwargs):
        for (k,v) in kwargs.items():
            setattr(self, k, v)

class TestDynamicBuild(unittest.TestCase):
    def setUp(self):
        config = basic_conf = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/test_config.yaml")
        Config.clear() # in case left unclean by a previous test case
        Config.init(config)

        import dynamicbuild

        self.base_dir = tempfile.mkdtemp()
        self.example_xproto = """option app_label = "exampleservice";
option name = "exampleservice";

message ExampleService (Service){
    option verbose_name = "Example Service";
    required string service_message = 1 [help_text = "Service Message to Display", max_length = 254, null = False, db_index = False, blank = False];
}

message Color (XOSBase){
     option verbose_name = "Color";
     required string name = 1 [help_text = "Name for this color", db_index = False, max_length = 256, null = False, blank = False];
     required string html_code = 2 [help_text = "Code for this color", db_index = False, max_length = 256, null = False, blank = False];
}

message ExampleServiceInstance (TenantWithContainer){
     option verbose_name = "Example Service Instance";
     required string tenant_message = 1 [help_text = "Tenant Message to Display", max_length = 254, null = False, db_index = False, blank = False];
     optional manytoone foreground_color->Color:serviceinstance_foreground_colors = 3 [db_index = True, null = True, blank = True];
     optional manytoone background_color->Color:serviceinstance_background_colors = 3 [db_index = True, null = True, blank = True];
}

message EmbeddedImage (XOSBase){
     option verbose_name = "Embedded Image";
     required string name = 1 [help_text = "Name for this image", db_index = False, max_length = 256, null = False, blank = False];
     required string url = 2 [help_text = "URL for this image", db_index = False, max_length = 256, null = False, blank = False];
     optional manytoone serviceinstance->ExampleServiceInstance:embedded_images = 3 [db_index = True, null = True, blank = True];
}
        """

        self.example_xproto_item = DynamicBuildItem(filename = "exampleservice.xproto",
                               contents = self.example_xproto)

        self.builder = dynamicbuild.DynamicBuilder(base_dir = self.base_dir)

    def tearDown(self):
        pass

    def test_pre_validate_file(self):
        self.builder.pre_validate_file(self.example_xproto_item)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
