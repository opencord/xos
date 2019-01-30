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

from __future__ import absolute_import
from setuptools import setup
import os
from shutil import copyfile


def version():
    # if not found, copy locally
    if not os.path.exists("VERSION"):
        copyfile("../../VERSION", "VERSION")
    with open("VERSION") as f:
        return f.read()


setup(
    name="XosSynchronizer",
    version=version(),
    description="XOS Synchronizer Framework",
    author="Scott Baker",
    author_email="scottb@opennetworking.org",
    packages=[
        "xossynchronizer",
        "xossynchronizer.steps",
        "xossynchronizer.event_steps",
        "xossynchronizer.pull_steps",
        "xossynchronizer.model_policies"
    ],
    install_requires=[
        "xosconfig>=2.1.35",
        "confluent-kafka>=0.11.5",
        "kafka>=0.11.5",
        "Jinja2>=2.10",
        "multistructlog>=2.1.0",
        "mock>=2.0.0",
        "networkx>=1.11",
    ],
    include_package_data=True,
)
