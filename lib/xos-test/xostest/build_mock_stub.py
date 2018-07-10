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
from xosgenx.generator import XOSProcessor

current_dir = os.path.dirname(os.path.realpath(__file__))

class Args:
    pass

class MockStub:

    @staticmethod
    def build(xprotos=[], **kwargs):
        """
        Generate a Fake Stub starting from a list of xproto files

        Arguments:
            xprotos {list[string]} -- A list of xproto file, they can be absolute path, or relative to "xos_dir"

        Keyword Arguments:
            * xos_dir {string} -- the absolute path to the XOS folder
            * output {string} -- the absolute path to the folder in which we want to generate the fake stub
        """

        if len(xprotos) == 0:
            raise ValueError("MockStub.build invoked with an empty list of xproto files")

        if not "xos_dir" in kwargs:
            raise ValueError("MockStub.build invoked without specifying xos_dir")

        xos_dir = kwargs["xos_dir"]
        output = kwargs["output"]

        files = []

        for xproto in xprotos:
            fn = None

            if os.path.isabs(xproto) and os.path.exists(xproto):
                fn = xproto
            elif os.path.exists(os.path.join(xos_dir, xproto)):
                fn = os.path.join(xos_dir, xproto)
            
            if not fn:
                raise ValueError("Xproto file %s does not exists" % xproto)

            files.append(fn)

        args = Args()
        args.output = output
        args.files = files
        args.target = os.path.join(current_dir, 'xtarget/mock_stub.xtarget')
        args.write_to_file = 'single'
        args.dest_file = 'fake_stub.py'

        XOSProcessor.process(args)
            
