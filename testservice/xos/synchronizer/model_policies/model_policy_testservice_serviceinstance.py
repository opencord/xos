# Copyright 2018-present Open Networking Foundation
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

import os
import sys

from synchronizers.new_base.policy import Policy

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import put_signal, wait_for_signal


class TestserviceServiceInstancePolicy(Policy):
    """
    TestserviceServiceInstancePolicy
    Implements model policy for TestserviceInstance
    """

    model_name = "TestserviceServiceInstance"

    def handle_create(self, si):
        self.logger.debug(
            "MODEL_POLICY: enter handle_create for TestserviceServiceInstance %s" %
            si.id)
        self.handle_update(si)
        # TODO: Implement creation policy, if it differs from update policy

    def handle_update(self, si):
        self.logger.info("TEST:POLICY_UPDATE_START", model=si)

        put_signal(log, model, "policy_start")

        if model.policy_after_sync or model.sync_during_policy:
            wait_for_signal(log, model, "sync_done")

        if model.policy_during_sync:
            wait_for_signal(log, model, "sync_start")

        if model.update_during_policy:
            model.some_other_integer = model.some_other_integer + 1
            model.save(update_fields=["some_other_integer"])

    def after_policy_save(self, model):
        put_signal(log, model, "policy_done")
        self.logger.info("TEST:POLICY_DONE", model=model)

    def handle_delete(self, si):
        self.logger.debug(
            "MODEL_POLICY: enter handle_delete for TestserviceServiceInstance %s" %
            si.id)
        # TODO: Implement delete policy
