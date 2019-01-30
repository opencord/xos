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
import os
from setuptools import setup
from shutil import copyfile

def version():
    # if not found, copy locally
    if not os.path.exists("VERSION"):
        copyfile("../../VERSION", "VERSION")
    with open("VERSION") as f:
        return f.read()


setup(
    name="XosGenX",
    version=version(),
    description="XOS Generative Toolchain",
    author="Sapan Bhatia, Matteo Scandolo",
    author_email="sapan@opennetworking.org, teo@opennetworking.org",
    packages=["xosgenx"],
    scripts=["bin/xosgenx"],
    install_requires=[
        "inflect>=1.0.1",
        "astunparse>=1.5.0",
    ],
    include_package_data=True,
)
