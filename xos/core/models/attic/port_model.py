
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


def can_update(self, user):
    if self.instance:
        return user.can_update_slice(self.instance.slice)
    if self.network:
        return user.can_update_slice(self.network.owner)
    return False

@staticmethod
def select_by_user(user):
    if user.is_admin:
        qs = Port.objects.all()
    else:
        instances = Instance.select_by_user(user)
        instance_ids = [instance.id for instance in instances]
        networks = Network.select_by_user(user)
        network_ids = [network.id for network in networks]
        qs = Port.objects.filter(Q(instance__in=instance_ids) | Q(network__in=network_ids))
    return qs

