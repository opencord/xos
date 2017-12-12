
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


import base64
import fnmatch
import os
import sys
import time
import traceback
from protos import dynamicload_pb2
from google.protobuf.empty_pb2 import Empty

from importlib import import_module

from xos.exceptions import *
from apihelper import XOSAPIHelperMixin, translate_exceptions

# The Tosca engine expects to be run from /opt/xos/tosca/ or equivalent. It
# needs some sys.path fixing up.
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
toscadir = os.path.join(currentdir, "../tosca")

class DynamicLoadService(dynamicload_pb2.dynamicloadServicer, XOSAPIHelperMixin):
    def __init__(self, thread_pool):
        self.thread_pool = thread_pool
        XOSAPIHelperMixin.__init__(self)

    def stop(self):
        pass

    @translate_exceptions
    def LoadModels(self, request, context):
        print "load models"

        response = dynamicload_pb2.LoadModelsReply()
        response.status = response.SUCCESS

        return response


