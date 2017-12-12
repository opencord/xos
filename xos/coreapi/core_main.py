
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


import os
import sys
import time

from reaper import ReaperThread
from grpc_server import XOSGrpcServer, restart_chameleon

from xosconfig import Config
from multistructlog import create_logger

Config.init()

log = create_logger(Config().get('logging'))

if __name__ == '__main__':
    server = XOSGrpcServer()
    server.init_core()
    server.init_django()
    server.start()

    reaper = ReaperThread()
    reaper.start()

    restart_chameleon()

    log.info("XOS core entering wait loop")

    _ONE_DAY_IN_SECONDS = 60 * 60 * 24
    try:
        while 1:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        log.info("XOS core terminated by keyboard interrupt")
        server.stop()
        reaper.stop()

