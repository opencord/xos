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

# Decorators that require django be imported/configured before they can be used

from __future__ import print_function
from django import db

from xosconfig import Config
from multistructlog import create_logger

log = create_logger(Config().get("logging"))


def check_db_connection(function):
    """ Check that the database connection is not in "already closed" state.
        This tends to happen when postgres is restarted. Connections will persist
        in this state throwing "connection already closed" errors until the
        old connections are disposed of.
    """
    def wrapper(self, *args, **kwargs):
        try:
            db.connection.cursor()
        except Exception as e:
            if "connection already closed" in str(e):
                log.warning("check_db_connection: connection already closed")
                try:
                    db.close_old_connections()
                    log.info("check_db_connection: removed old connections")
                except Exception as e:
                    log.exception("check_db_connection: we failed to fix the failure", e=e)
                    raise
            else:
                raise

        result = function(self, *args, **kwargs)
        return result

    return wrapper

