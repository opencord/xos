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


from xosapi.orm import ORMWrapper, register_convenience_wrapper

class ORMWrapperServiceInstance(ORMWrapper):
    @property
    def westbound_service_instances(self):
        links = self.provided_links.all()
        instances = []
        for link in links:
            instances.append(link.subscriber_service_instance.leaf_model)

        return instances

    def get_westbound_service_instance_properties(self, prop_name):
        wi = self.westbound_service_instances

        if len(wi) == 0:
            raise Exception('ServiceInstance %s has no westbound service instances')

        for i in wi:
            if hasattr(prop_name, i):
                return getattr(i, prop_name)
            else:
                return i.get_westbound_service_instance_properties(prop_name)

register_convenience_wrapper("ServiceInstance", ORMWrapperServiceInstance)