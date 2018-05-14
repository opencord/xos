
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

import imp
import inspect
import os
import threading
from xosconfig import Config
from multistructlog import create_logger

log = create_logger(Config().get('logging'))

class XOSKafkaThread(threading.Thread):
    def __init__(self, step, *args, **kwargs):
        super(XOSKafkaThread, self).__init__(*args, **kwargs)
        self.bootstrap_servers = ["container-vnf-kafka"]
        self.consumer = None
        self.step = step
        self.daemon = True

    def run(self):
        from kafka import KafkaConsumer
        self.consumer = KafkaConsumer(bootstrap_servers=self.bootstrap_servers)
        if self.step.topics:
            self.consumer.subscribe(self.step.topics)
        elif self.step.pattern:
            self.consumer.subscriber(self.step.pattern)
        else:
            raise Exception("Neither topics nor pattern is defined")

        log.info("Waiting for events", topic=self.step.topics, pattern=self.step.pattern)
        for msg in self.consumer:
            log.info("Processing event", event=msg)
            self.step().process_event(msg)

class XOSEventEngine:
    def __init__(self):
        self.event_steps = []
        self.threads = []

    def start(self):
        for step in self.event_steps:
            if step.technology == "kafka":
                thread = XOSKafkaThread(step)
                thread.start()
                self.threads.append(thread)
            else:
                raise Exception("Unknown technology %s" % step.technology)

    def load_event_step_modules(self, event_step_dir):
        self.event_steps = []
        log.info("Loading event steps", pull_step_dir=event_step_dir)

        # NOTE we'll load all the classes that inherit from EventStep
        for fn in os.listdir(event_step_dir):
            pathname = os.path.join(event_step_dir, fn)
            if os.path.isfile(pathname) and fn.endswith(".py") and (fn != "__init__.py") and ("test" not in fn):
                event_module = imp.load_source(fn[:-3], pathname)

                for classname in dir(event_module):
                    c = getattr(event_module, classname, None)

                    if inspect.isclass(c):
                        base_names = [b.__name__ for b in c.__bases__]
                        if 'EventStep' in base_names:
                            self.event_steps.append(c)
        log.info("Loaded event steps", steps=self.event_steps)
        return self.event_steps
