
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

# Look for a VERSION number in the same directory as setup.py. If that's
# not found, then assume we're in the xos build tree and look for it in
# the root of the repository.

file_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
__version_filename__ = os.path.join(file_path, "VERSION")
if not os.path.exists(__version_filename__):
    __version_filename__ = os.path.join(file_path, "../../../VERSION")

__version__ = open(__version_filename__, "rt").readline().strip()
