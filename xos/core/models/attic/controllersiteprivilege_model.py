
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
    if user.is_readonly:
        return False
    if user.is_admin:
        return True

    cprivs = ControllerPrivilege.objects.filter(privilege__accessor_id=user.id, privilege__object_type='Site')
    for cpriv in cprivs:
        if cpriv.privilege.permission in ['role:admin', 'role:Admin']:
            return True
    return False

@staticmethod
def select_by_user(user):
    if user.is_admin:
        qs = ControllerPrivilege.objects.filter(privilege__object_type='Site')
    else:
        cpriv_ids = [cp.id for cp in ControllerPrivilege.objects.filter(privilege__accessor_id=user.id, privilege__object_type='Site')]
        qs = ControllerPrivilege.objects.filter(id__in=cpriv_ids, privilege__object_type='Site')
    return qs
