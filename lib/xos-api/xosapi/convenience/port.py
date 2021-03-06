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

from __future__ import absolute_import

from xosapi.orm import ORMWrapper, register_convenience_wrapper


class ORMWrapperPort(ORMWrapper):
    def get_parameters(self):
        parameter_dict = {}

        for param in self.stub.NetworkParameter.objects.filter(
            content_type=self.self_content_type_id, object_id=self.id
        ):
            parameter_dict[param.parameter.name] = param.value

        return parameter_dict


register_convenience_wrapper("Port", ORMWrapperPort)
