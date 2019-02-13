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

from protos import dynamicload_pb2
from protos import dynamicload_pb2_grpc

from xosutil.autodiscover_version import autodiscover_version_of_main
from dynamicbuild import DynamicBuilder
from apistats import REQUEST_COUNT, track_request_time
import grpc


class DynamicLoadService(dynamicload_pb2_grpc.dynamicloadServicer):
    def __init__(self, thread_pool, server):
        self.thread_pool = thread_pool
        self.server = server
        self.django_apps = None
        self.django_apps_by_name = {}

    def stop(self):
        pass

    def set_django_apps(self, django_apps):
        """ Allows the creator of DynamicLoadService to pass in a pointer to django's app list once django has been
            installed. This is optional. We don't import django.apps directly, as DynamicLoadService must be able
            to run even if django is broken due to modeling issues.
        """
        self.django_apps = django_apps

        # Build up some dictionaries used by the API handlers. We can build these once at initialization time because
        # when apps are onboarded, the core is always restarted.

        self.django_apps_by_name = {}
        self.django_app_models = {}
        if self.django_apps:
            for app in self.django_apps.get_app_configs():
                self.django_apps_by_name[app.name] = app

                # Build up a dictionary of all non-decl models.
                django_models = {}
                for (k, v) in app.models:
                    if not k.endswith("_decl"):
                        django_models[k] = v
                self.django_app_models[app.name] = django_models

    @track_request_time("DynamicLoad", "LoadModels")
    def LoadModels(self, request, context):
        try:
            builder = DynamicBuilder()
            result = builder.handle_loadmodels_request(request)

            if result == builder.SOMETHING_CHANGED:
                self.server.delayed_shutdown(5)

            response = dynamicload_pb2.LoadModelsReply()
            response.status = response.SUCCESS
            REQUEST_COUNT.labels(
                "xos-core", "DynamicLoad", "LoadModels", grpc.StatusCode.OK
            ).inc()
            return response
        except Exception as e:
            import traceback

            traceback.print_exc()
            REQUEST_COUNT.labels(
                "xos-core", "DynamicLoad", "LoadModels", grpc.StatusCode.INTERNAL
            ).inc()
            raise e

    @track_request_time("DynamicLoad", "UnloadModels")
    def UnloadModels(self, request, context):
        try:
            builder = DynamicBuilder()
            result = builder.handle_unloadmodels_request(request, self.django_app_models[request.name])

            if result == builder.SOMETHING_CHANGED:
                self.server.delayed_shutdown(5)

            response = dynamicload_pb2.LoadModelsReply()
            response.status = response.SUCCESS
            REQUEST_COUNT.labels(
                "xos-core", "DynamicLoad", "UnloadModels", grpc.StatusCode.OK
            ).inc()
            return response
        except Exception as e:
            import traceback

            traceback.print_exc()
            REQUEST_COUNT.labels(
                "xos-core", "DynamicLoad", "UnloadModels", grpc.StatusCode.INTERNAL
            ).inc()
            raise e

    @track_request_time("DynamicLoad", "GetLoadStatus")
    def GetLoadStatus(self, request, context):
        try:
            builder = DynamicBuilder()
            manifests = builder.get_manifests()

            response = dynamicload_pb2.LoadStatusReply()
            response.model_status = self.server.model_status
            response.model_output = self.server.model_output
            for manifest in manifests:
                item = response.services.add()
                item.name = manifest["name"]
                item.version = manifest["version"]
                item.state = manifest.get("state", "unspecified")

                if item.state == "load":
                    django_app = self.django_apps_by_name.get("services." + item.name)
                    if django_app:
                        item.state = "present"
                        # TODO: Might be useful to return a list of models as well

            # the core is always onboarded, so doesn't have an explicit manifest
            item = response.services.add()
            item.name = "core"
            item.version = autodiscover_version_of_main()
            if "core" in self.django_apps_by_name:
                item.state = "present"
            else:
                item.state = "load"
            REQUEST_COUNT.labels(
                "xos-core", "DynamicLoad", "GetLoadStatus", grpc.StatusCode.OK
            ).inc()
            return response
        except Exception as e:
            import traceback

            traceback.print_exc()
            REQUEST_COUNT.labels(
                "xos-core", "DynamicLoad", "GetLoadStatus", grpc.StatusCode.INTERNAL
            ).inc()
            raise e

    @track_request_time("DynamicLoad", "GetConvenienceMethods")
    def GetConvenienceMethods(self, request, context):
        # self.authenticate(context, required=True)
        try:
            builder = DynamicBuilder()
            manifests = builder.get_manifests()

            response = dynamicload_pb2.ListConvenienceMethodsReply()

            for manifest in manifests:
                for cm in manifest["convenience_methods"]:
                    item = response.convenience_methods.add()
                    item.filename = cm["filename"]
                    item.contents = open(cm["path"]).read()
            REQUEST_COUNT.labels(
                "xos-core", "DynamicLoad", "GetConvenienceMethods", grpc.StatusCode.OK
            ).inc()
            return response

        except Exception as e:
            import traceback

            traceback.print_exc()
            REQUEST_COUNT.labels(
                "xos-core",
                "DynamicLoad",
                "GetConvenienceMethods",
                grpc.StatusCode.INTERNAL,
            ).inc()
            raise e
