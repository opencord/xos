import unittest
import os
from xosgen.generator import XOSGenerator

BASE_XPROTO = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/test_xproto/base.xproto")
BASE_TARGET = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/test_xproto/base.xtarget")
OUTPUT_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/test_xproto/out/")

class Args:
    pass

class XOSGeneratorTest(unittest.TestCase):
    """
    Testing the XOS Generative Toolchain
    """

    def setUp(self):
        filesToRemove = [f for f in os.listdir(OUTPUT_DIR)]
        for f in filesToRemove:
            os.remove(OUTPUT_DIR + '/' + f)

    def test_generator(self):
        """
        [XOS-GenX] Generate TOSCA from base.xproto  
        """
        args = Args()
        args.inputs = [BASE_XPROTO]
        args.target = BASE_TARGET
        args.output = OUTPUT_DIR
        generator = XOSGenerator(args)
        generator.generate()
        generatedFiles = [f for f in os.listdir(OUTPUT_DIR)]
        self.assertEqual(len(generatedFiles), len(args.inputs))

