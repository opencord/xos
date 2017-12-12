
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

class DynamicBuilder(object):
    def __init__(self):
        self.services_dir = "/opt/xos/dynamic_services"

    def pre_validate_file(self, item):
        # someone might be trying to trick us into writing files outside the designated directory
        if "/" in item.filename:
            raise Exception("illegal character in filename %s" % request.filename)

    def pre_validate_models(self, request):
        # do whatever validation we can before saving the files
        for item in request.xprotos:
            self.pre_validate_file(item)

        for item in request.decls:
            self.pre_validate_file(item)

        for item in request.attics:
            self.pre_validate_file(item)


    def save_models(self, request):
        self.pre_validate_models(request)

        all_filenames = []

        service_dir = os.path.join(self.services_dir, request.name)
        if not os.path.exists(service_dir):
            os.makedirs(service_dir)

        for item in request.xprotos:
            all_filenames.append(item.filename)
            file(os.path.join(service_dir, item.filename), "w").write(item.contents)

        for item in request.decls:
            all_filenames.append(item.filename)
            file(os.path.join(service_dir, item.filename), "w").write(item.contents)

        if request.attics:
            attic_dir = os.path.join(service_dir, "attic")
            if not os.path.exists(attic_dir):
                os.makedirs(attic_dir)
            for item in request.attics:
                all_filenames.append(os.path.join("attic", item.filename))
                file(os.path.join(attic_dir, item.filename), "w").write(item.contents)
