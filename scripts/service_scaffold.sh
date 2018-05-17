#!/usr/bin/env bash

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

# service_scaffold.sh
# creates a directories and scaffolding for a service

set -e -o pipefail

if [ -z "${SERVICE_NAME}" ];
then
  SERVICE_NAME=$(basename "${PWD}")
  echo "SERVICE_NAME undefined, using parent directory name, "
fi

if [ -z "${SERVICE_VERSION}" ];
then
  SERVICE_VERSION="0.0.1.dev0"
  echo "SERVICE_VERSION undefined, using ${SERVICE_VERSION}"
fi

echo "Creating service named: ${SERVICE_NAME}, version: ${SERVICE_VERSION}"

# create uppercase version of SERVICE_NAME in a naive fashion
UC_SERVICE_NAME=$(echo "${SERVICE_NAME}" | cut -c1 | tr '[:lower:]' '[:upper:]')$(echo "${SERVICE_NAME}" | cut -c2-)

echo "Uppercase service name: ${UC_SERVICE_NAME}"

echo "Creating directories"
mkdir -p xos/synchronizer/model_policies/
mkdir -p xos/synchronizer/models/
mkdir -p xos/synchronizer/pull_steps/
mkdir -p xos/synchronizer/steps/
mkdir -p xos/synchronizer/tests/

echo "Creating empty model-deps"
echo "{}" > xos/synchronizer/model-deps

echo "Creating xproto scaffold"
cat << EOF > "xos/synchronizer/models/${SERVICE_NAME}.xproto"
option app_label = "${SERVICE_NAME}";
option name = "${SERVICE_NAME}";

message ${UC_SERVICE_NAME}Service (Service){
  option verbose_name = "${UC_SERVICE_NAME} Service";
}

EOF

echo "Creating service config.yaml"
cat << EOF > "xos/synchronizer/${SERVICE_NAME}_config.yaml"
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

name: ${SERVICE_NAME}
accessor:
  username: xosadmin@opencord.org
  password: "@/opt/xos/services/${SERVICE_NAME}/credentials/xosadmin@opencord.org"
required_models:
  - ${UC_SERVICE_NAME}Service
dependency_graph: "/opt/xos/synchronizers/${SERVICE_NAME}/model-deps"
model_policies_dir: "/opt/xos/synchronizers/${SERVICE_NAME}/model_policies"
models_dir: "/opt/xos/synchronizers/${SERVICE_NAME}/models"
pull_steps_dir: "/opt/xos/synchronizers/${SERVICE_NAME}/pull_steps"
steps_dir: "/opt/xos/synchronizers/${SERVICE_NAME}/steps"
sys_dir: "/opt/xos/synchronizers/${SERVICE_NAME}/sys"
EOF

echo "Creating synchronizer.py"
cat << EOF > "xos/synchronizer/${SERVICE_NAME}-synchronizer.py"
#!/usr/bin/env python

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

"""
${SERVICE_NAME}-synchronizer.py
This is the main entrypoint for the synchronizer. It loads the config file, and
then starts the synchronizer.
"""

import importlib
import logging
import os
import sys
from xosconfig import Config

config_file = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/${SERVICE_NAME}_config.yaml')
Config.init(config_file, 'synchronizer-config-schema.yaml')

synchronizer_path = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "../../synchronizers/new_base")

sys.path.append(synchronizer_path)
mod = importlib.import_module("xos-synchronizer")
mod.main()
EOF

chmod +x "xos/synchronizer/${SERVICE_NAME}-synchronizer.py"

echo "Creating synchronizer Dockerfile"
cat << EOF > Dockerfile.synchronizer
# Copyright $(date +%Y)-present Open Networking Foundation
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

# xosproject/${SERVICE_NAME}

FROM xosproject/xos-synchronizer-base:candidate

COPY xos/synchronizer /opt/xos/synchronizers/${SERVICE_NAME}
COPY VERSION /opt/xos/synchronizers/${SERVICE_NAME}/

ENTRYPOINT []

WORKDIR "/opt/xos/synchronizers/${SERVICE_NAME}"

# Label image
ARG org_label_schema_schema_version=1.0
ARG org_label_schema_name=${SERVICE_NAME}
ARG org_label_schema_version=unknown
ARG org_label_schema_vcs_url=unknown
ARG org_label_schema_vcs_ref=unknown
ARG org_label_schema_build_date=unknown
ARG org_opencord_vcs_commit_date=unknown
ARG org_opencord_component_chameleon_version=unknown
ARG org_opencord_component_chameleon_vcs_url=unknown
ARG org_opencord_component_chameleon_vcs_ref=unknown
ARG org_opencord_component_xos_version=unknown
ARG org_opencord_component_xos_vcs_url=unknown
ARG org_opencord_component_xos_vcs_ref=unknown

LABEL org.label-schema.schema-version=\$org_label_schema_schema_version \\
      org.label-schema.name=\$org_label_schema_name \\
      org.label-schema.version=\$org_label_schema_version \\
      org.label-schema.vcs-url=\$org_label_schema_vcs_url \\
      org.label-schema.vcs-ref=\$org_label_schema_vcs_ref \\
      org.label-schema.build-date=\$org_label_schema_build_date \\
      org.opencord.vcs-commit-date=\$org_opencord_vcs_commit_date \\
      org.opencord.component.chameleon.version=\$org_opencord_component_chameleon_version \\
      org.opencord.component.chameleon.vcs-url=\$org_opencord_component_chameleon_vcs_url \\
      org.opencord.component.chameleon.vcs-ref=\$org_opencord_component_chameleon_vcs_ref \\
      org.opencord.component.xos.version=\$org_opencord_component_xos_version \\
      org.opencord.component.xos.vcs-url=\$org_opencord_component_xos_vcs_url \\
      org.opencord.component.xos.vcs-ref=\$org_opencord_component_xos_vcs_ref

CMD "python ${SERVICE_NAME}-synchronizer.py"
EOF

echo "Creating sync step"
cat << EOF > "xos/synchronizer/steps/sync_${SERVICE_NAME}.py"
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

from synchronizers.new_base.syncstep import SyncStep
from synchronizers.new_base.modelaccessor import Service

from xosconfig import Config
from multistructlog import create_logger

log = create_logger(Config().get('logging'))

class Sync${UC_SERVICE_NAME}Service(SyncStep):
    """
    Sync${UC_SERVICE_NAME}Service
    Implements sync step for syncing ${UC_SERVICE_NAME} Services
    """

    provides = [${UC_SERVICE_NAME}Service]
    observes = ${UC_SERVICE_NAME}Service
    requested_interval = 0

    def __init__(self, *args, **kwargs):
        super(Sync${UC_SERVICE_NAME}Service, self).__init__(*args, **kwargs)

    def sync_record(self, model):
        # TODO: Implement sync step
        pass

    def delete_record(self, model):
        # TODO: Implement delete step
        pass
EOF
