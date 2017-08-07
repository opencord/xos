
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
    return user.can_update_deployment(self)

@staticmethod
def select_by_user(user):
    from core.models.deploymentprivilege import DeploymentPrivilege
    if user.is_admin:
        qs = DeploymentPrivilege.objects.all()
    else:
        dpriv_ids = [dp.id for dp in DeploymentPrivilege.objects.filter(user=user)]
        qs = DeploymentPrivilege.objects.filter(id__in=dpriv_ids)
    return qs
