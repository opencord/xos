import unittest
import os
from xosgen.generator import XOSGenerator

BASE_XPROTO = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/test_xproto/base.xproto")
BASE_TARGET = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/test_xproto/base.xtarget")
OUTPUT_FILE = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/test_xproto/out.yaml")

class Args:
    pass

class XOSGeneratorTest(unittest.TestCase):
    """
    Testing the XOS Generative Toolchain
    """

    def test_generator(self):
        """
        [XOS-GenX] Generate TOSCA from base.xproto  
        """
        args = Args()
        args.inputs = [BASE_XPROTO]
        args.target = BASE_TARGET
        args.output = OUTPUT_FILE
        generator = XOSGenerator(args)
        generator.generate()

