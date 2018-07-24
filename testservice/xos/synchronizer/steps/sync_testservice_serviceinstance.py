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
import time
from synchronizers.new_base.syncstep import SyncStep
from synchronizers.new_base.modelaccessor import TestserviceServiceInstance

from xosconfig import Config
from multistructlog import create_logger

log = create_logger(Config().get('logging'))

def get_signal_fn(model, name):
    return os.path.join("/tmp", "signal_%s_%s" % (model.__class__.__name__, model.id))

def put_signal(log, model, name):
    open(get_signal_fn(model, name), "a").write( time.time() )

def wait_for_signal(log, model, name, timeout=30):
    fn = get_signal_fn(model, name)
    count = 0
    while not os.path.exists(fn):
        count+=1
        if (count>30):
            log.error("TEST:FAIL - Timeout waiting for %s" % fn, model=model)
            raise Exception("timeout")
        time.sleep(1)

class SyncTestserviceServiceInstance(SyncStep):
    """
    SyncTestserviceServiceInstance
    Implements sync step for syncing Testservice Services
    """

    provides = [TestserviceServiceInstance]
    observes = [TestserviceServiceInstance]
    requested_interval = 0

    def sync_record(self, model):
        log.info("TEST:SYNC_START", model=model)

        put_signal(log, model, "sync_start")

        if model.sync_after_policy or model.policy_during_sync:
            wait_for_signal(log, model, "policy_done")

        if model.sync_during_policy:
            wait_for_signal(log, model, "policy_start")

        if model.update_during_sync:
            model.some_integer = model.some_integer+1
            model.save(update_fields = ["some_integer"])

    def after_sync_save(self, model):
        put_signal(log, model, "sync_done")
        log.info("TEST:SYNC_DONE", model=model)

    def delete_record(self, model):
        log.info("Deleting TestserviceServiceInstance",
                 object=str(model))
        # TODO: Implement delete step
