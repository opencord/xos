
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


#!/usr/bin/env python

try:
    from xosutil.autodiscover_version import autodiscover_version_of_caller
    autodiscover_version_of_caller(save_to="xosconfig/version.py")
except ImportError:
    # xosutil is not installed
    pass

from xosconfig.version import __version__

setup(name='XosConfig',
      version=__version__,
      description='XOS Config Library',
      author='Matteo Scandolo',
      author_email='teo@onlab.us',
      packages=['xosconfig'],
      include_package_data=True
     )
