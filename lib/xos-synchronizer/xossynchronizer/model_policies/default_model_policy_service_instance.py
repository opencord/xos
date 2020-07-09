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


from xossynchronizer.modelaccessor import ServiceInstance, ServiceInstanceLink, model_accessor
from xossynchronizer.model_policies.policy import Policy

from xosconfig import Config
from multistructlog import create_logger

log = create_logger(Config().get('logging'))

class DefaultServiceInstancePolicy(Policy):
    model_name = "ServiceInstance"

    @staticmethod
    def resync(si):
        service = si.owner
        links = service.subscribed_dependencies.all()
        for link in links:
            provider_service = link.provider_service.leaf_model
            valid_provider_service_instance = provider_service.validate_links(si)
            if not valid_provider_service_instance:
                continue
            else:
                valid_provider_service_instance.save(always_update_timestamp = True)

    def handle_create(self, si):
        return self.handle_update(si)

    def handle_update(self, si):
        log.info("Handle_update for Service Instance", service_instance=si)
        DefaultServiceInstancePolicy.resync(si)

    def handle_delete(self, si):
        log.info("Handle_delete for Service Instance", service_instance=si)
