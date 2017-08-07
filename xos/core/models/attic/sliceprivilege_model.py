
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
    return user.can_update_slice(self.slice)

@staticmethod
def select_by_user(user):
    if user.is_admin:
        qs = SlicePrivilege.objects.all()
    else:
        # You can see your own SlicePrivileges
        sp_ids = [sp.id for sp in SlicePrivilege.objects.filter(user=user)]

        from core.models.siteprivilege import SitePrivilege
        # A site pi or site admin can see the SlicePrivileges for all slices in his Site
        for priv in SitePrivilege.objects.filter(user=user):
            if priv.role.role in ['pi', 'admin']:
                sp_ids.extend( [sp.id for sp in SlicePrivilege.objects.filter(slice__site = priv.site)] )

        # A slice admin can see the SlicePrivileges for his Slice
        for priv in SlicePrivilege.objects.filter(user=user, role__role="admin"):
            sp_ids.extend( [sp.id for sp in SlicePrivilege.objects.filter(slice=priv.slice)] )

        qs = SlicePrivilege.objects.filter(id__in=sp_ids)
    return qs
