
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

import json
import os
from xosgenx.generator import XOSGenerator

class DynamicBuilder(object):
    def __init__(self):
        self.services_dir = "/opt/xos/dynamic_services"
        self.manifest_dir = "/opt/xos/dynamic_services/manifests"
        self.services_dest_dir = "/opt/xos/services_gen"

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

        service_dir = os.path.join(self.services_dir, request.name)
        if not os.path.exists(service_dir):
            os.makedirs(service_dir)

        if not os.path.exists(self.manifest_dir):
            os.makedirs(self.manifest_dir)

        manifest_fn = os.path.join(self.manifest_dir, request.name + ".json")
        if os.path.exists(manifest_fn):
            os.remove(manifest_fn)

        # convert the request to a manifest, so we can save it
        service_manifest = {"name": request.name,
                            "dir": service_dir,
                            "dest_dir": os.path.join(self.services_dest_dir, request.name),
                            "xprotos": [],
                            "decls": [],
                            "attics": []}

        for item in request.xprotos:
            file(os.path.join(service_dir, item.filename), "w").write(item.contents)
            service_manifest["xprotos"].append({"filename": item.filename})

        for item in request.decls:
            file(os.path.join(service_dir, item.filename), "w").write(item.contents)
            service_manifest["decls"].append({"filename": item.filename})

        if request.attics:
            attic_dir = os.path.join(service_dir, "attic")
            service_manifest["attic_dir"] = attic_dir
            if not os.path.exists(attic_dir):
                os.makedirs(attic_dir)
            for item in request.attics:
                file(os.path.join(attic_dir, item.filename), "w").write(item.contents)
                service_manifest["attics"].append({"filename": item.filename})

        file(manifest_fn, "w").write(json.dumps(service_manifest))

        return service_manifest

    def run_xosgenx_service(self, manifest):
        if not os.path.exists(manifest["dir"]):
            os.makedirs(manifest["dir"])

        xproto_filenames = [x["filename"] for x in manifest["xprotos"]]

        class Args:
            pass

        # Generate models
        is_service = manifest["name"] != 'core'

        args = Args()
        args.output = manifest["dest_dir"]
        args.attic = manifest["dir"] + '/attic'
        args.files = xproto_filenames

        if is_service:
            args.target = 'service.xtarget'
            args.write_to_file = 'target'
        else:
            args.target = 'django.xtarget'
            args.dest_extension = 'py'
            args.write_to_file = 'model'

        XOSGenerator.generate(args)

        # Generate security checks
        class SecurityArgs:
            output = manifest["dest_dir"]
            target = 'django-security.xtarget'
            dest_file = 'security.py'
            write_to_file = 'single'
            files = xproto_filenames

        XOSGenerator.generate(SecurityArgs())

        # Generate __init__.py
        if service_name == "core":
            class InitArgs:
                output = manifest["dest_dir"]
                target = 'init.xtarget'
                dest_file = '__init__.py'
                write_to_file = 'single'
                files = xproto_filenames

            XOSGenerator.generate(InitArgs())
