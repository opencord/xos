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

import inspect
from apistats import REQUEST_COUNT, track_request_time
import grpc
from authhelper import XOSAuthHelperMixin
from decorators import translate_exceptions, require_authentication
from xos.exceptions import XOSNotAuthenticated
from core.models import ServiceInstance
from django.db.models import F, Q
import django.apps
from django.contrib.auth import authenticate as django_authenticate
import fnmatch
import os
import sys
import traceback
from protos import filetransfer_pb2, filetransfer_pb2_grpc

from importlib import import_module
from django.conf import settings

SessionStore = import_module(settings.SESSION_ENGINE).SessionStore


class FileTransferService(filetransfer_pb2_grpc.filetransferServicer, XOSAuthHelperMixin):
    def __init__(self, thread_pool):
        self.thread_pool = thread_pool
        XOSAuthHelperMixin.__init__(self)

    def stop(self):
        pass

    @translate_exceptions("FileTransfer", "Download")
    @track_request_time("FileTransfer", "Download")
    @require_authentication
    def Download(self, request, context):
        if not request.uri.startswith("file://"):
            raise Exception("Uri must start with file://")

        backend_filename = request.uri[7:]
        if not os.path.exists(backend_filename):
            raise Exception("File %s does not exist" % backend_filename)

        with open(backend_filename) as backend_f:
            chunk = backend_f.read(65536)
            yield filetransfer_pb2.FileContents(chunk=chunk)
