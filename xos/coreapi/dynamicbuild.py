
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
import hashlib
import os
from xosgenx.generator import XOSGenerator

from xosconfig import Config
from multistructlog import create_logger
log = create_logger(Config().get('logging'))

def makedirs_if_noexist(pathname):
    if not os.path.exists(pathname):
        os.makedirs(pathname)

class DynamicBuilder(object):
    def __init__(self):
        self.services_dir = "/opt/xos/dynamic_services"
        self.manifest_dir = "/opt/xos/dynamic_services/manifests"
        self.services_dest_dir = "/opt/xos/services"
        self.protos_dir = "/opt/xos/coreapi/protos"
        self.app_metadata_dir = "/opt/xos/xos"

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

    def handle_loadmodels_request(self, request):
        manifest_fn = os.path.join(self.manifest_dir, request.name + ".json")
        if os.path.exists(manifest_fn):
            try:
                manifest = json.loads(open(manifest_fn).read())
            except:
                log.exception("Error loading old manifest", filename=manifest_fn)
                manifest = {}
        else:
            manifest = {}

        # TODO: Check version number to make sure this is not a downgrade ?

        hash = self.generate_request_hash(request)
        if hash == manifest.get("hash"):
            # The hash of the incoming request is identical to the manifest that we have saved, so this request is a
            # no-op.
            log.info("Models are already up-to-date; skipping dynamic load.", name=request.name)
            return

        self.pre_validate_models(request)

        manifest = self.save_models(request, hash=hash)

        self.run_xosgenx_service(manifest)

        log.debug("Saving service manifest", name=request.name)
        file(manifest_fn, "w").write(json.dumps(manifest))

        log.info("Finished LoadModels request", name=request.name)

        # TODO: schedule a restart

    def generate_request_hash(self, request):
        # TODO: could we hash the request rather than individually hashing the subcomponents of the request?
        m = hashlib.sha1()
        m.update(request.name)
        m.update(request.version)
        for item in request.xprotos:
            m.update(item.filename)
            m.update(item.contents)
        for item in request.decls:
            m.update(item.filename)
            m.update(item.contents)
        for item in request.decls:
            m.update(item.filename)
            m.update(item.contents)
        return m.hexdigest()

    def save_models(self, request, hash=None):
        if not hash:
            hash = self.generate_request_hash(request)

        service_dir = os.path.join(self.services_dir, request.name)
        if not os.path.exists(service_dir):
            os.makedirs(service_dir)

        if not os.path.exists(self.manifest_dir):
            os.makedirs(self.manifest_dir)

        manifest_fn = os.path.join(self.manifest_dir, request.name + ".json")

        # Invariant is that if a manifest file exists, then it accurately reflects that has been stored to disk. Since
        # we're about to potentially overwrite files, destroy the old manifest.
        if os.path.exists(manifest_fn):
            os.remove(manifest_fn)

        # convert the request to a manifest, so we can save it
        service_manifest = {"name": request.name,
                            "version": request.version,
                            "hash": hash,
                            "dir": service_dir,
                            "manifest_fn": manifest_fn,
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

        return service_manifest

    def run_xosgenx_service(self, manifest):
        if not os.path.exists(manifest["dest_dir"]):
            os.makedirs(manifest["dest_dir"])

        xproto_filenames = [os.path.join(manifest["dir"], x["filename"]) for x in manifest["xprotos"]]

        class Args:
            pass

        # Generate models
        is_service = manifest["name"] != 'core'

        args = Args()
        args.output = manifest["dest_dir"]
        args.attic = os.path.join(manifest["dir"], 'attic')
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
        if manifest["name"] == "core":
            class InitArgs:
                output = manifest["dest_dir"]
                target = 'init.xtarget'
                dest_file = '__init__.py'
                write_to_file = 'single'
                files = xproto_filenames

            XOSGenerator.generate(InitArgs())

    def build_the_core(self):
        self.generate_app_lists()
        self.build_protos()

    def generate_app_lists(self):
        # TODO: Once static onboarding is no more, we will get these from the manifests rather than using listdir

        app_names = []
        for fn in os.listdir(self.services_dest_dir):
            service_dir = os.path.join(self.services_dest_dir, fn)
            if (not fn.startswith(".")) and os.path.isdir(service_dir):
                models_fn = os.path.join(service_dir, "models.py")
                if os.path.exists(models_fn):
                    if fn=="syndicate_storage":
                        continue
                    app_names.append(fn)

        # Generate the migration list
        mig_list_fn = os.path.join(self.app_metadata_dir, "xosbuilder_migration_list")
        makedirs_if_noexist(os.path.dirname(mig_list_fn))
        file(mig_list_fn, "w").write("\n".join(app_names)+"\n")

        # Generate the app list
        app_list_fn = os.path.join(self.app_metadata_dir, "xosbuilder_app_list")
        makedirs_if_noexist(os.path.dirname(app_list_fn))
        file(app_list_fn, "w").write("\n".join(["services.%s" % x for x in app_names])+"\n")

    def build_protos(self):
        # TODO: replace this with something that runs xosgenx directly
        result = os.system("cd %s && make rebuild-protos" % self.protos_dir)
        if result != 0:
            raise Exception("failed to run `make rebuild-protos`")

        # TODO: replace this with something that runs protoc directly
        result = os.system("cd %s && make" % self.protos_dir)
        if result != 0:
            raise Exception("failed to run `make`")
