
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

# Look for a VERSION number in the same directory as setup.py. If that's
# not found, then assume we're in the xos build tree and look for it in
# the root of the repository.
setup_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
version_file = os.path.join(setup_path, "VERSION")
if not os.path.exists(version_file):
    version_file = os.path.join(setup_path, "../../VERSION")
version = open(version_file, "rt").readline().strip()

from setuptools import setup

setup(name='XosConfig',
      version=version,
      description='XOS Config Library',
      author='Matteo Scandolo',
      author_email='teo@onlab.us',
      packages=['xosconfig'],
      include_package_data=True
     )
