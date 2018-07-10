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

class XProtoLocator:
    @staticmethod
    def get_xproto_path(services_dir, service_name, xproto_name):
        """Get the absolute path for an xproto file
        
        Arguments:
            service_dir {[type]} -- [description]
            service_name {[type]} -- [description]
            xproto_name {[type]} -- [description]
        """
        name = os.path.join(service_name, "xos", xproto_name)
        if os.path.exists(os.path.join(services_dir, name)):
            return os.path.join(services_dir, name)
        else:
            name = os.path.join(service_name, "xos", "synchronizer", "models", xproto_name)
            if os.path.exists(os.path.join(services_dir, name)):
                return os.path.join(services_dir, name)
        raise Exception("Unable to find service=%s xproto=%s" % (service_name, xproto_name))
