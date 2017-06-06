import unittest
import os
from xosgen.generator import XOSGenerator
from test_xproto.expected_output import TOSCA_EXPECTED_OUTPUT, TEST_EXPECTED_OUTPUT, DJANGO_EXPECTED_OUTPUT

BASE_XPROTO = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/test_xproto/base.xproto")
TEST_TARGET = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/test_xproto/test.xtarget")
OUTPUT_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/test_xproto/out/")

TEST_ATTICS = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/test_xproto/attics/")


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

    def test_generator_custom_target(self):
        """
        [XOS-GenX] Generate output from base.xproto  
        """
        args = Args()
        args.inputs = [BASE_XPROTO]
        args.target = TEST_TARGET
        args.output = OUTPUT_DIR
        generator = XOSGenerator(args)
        output = generator.generate()
        self.assertEqual(output, TEST_EXPECTED_OUTPUT)

    def test_generator_tosca(self):
        """
        [XOS-GenX] Generate TOSCA from base.xproto, and write to file
        """
        args = Args()
        args.inputs = [BASE_XPROTO]
        args.target = 'tosca.xtarget'
        args.output = OUTPUT_DIR
        generator = XOSGenerator(args)
        generator.generate()
        generated_files = [f for f in os.listdir(OUTPUT_DIR)]
        self.assertEqual(len(generated_files), len(args.inputs))
        generated_file = OUTPUT_DIR + '/' + generated_files[0];
        output = open(generated_file, "r").read()
        self.assertEqual(output, TOSCA_EXPECTED_OUTPUT)

    def test_django_with_attic(self):
        """
        [XOS-GenX] Generate output from base.xproto  
        """
        args = Args()
        args.inputs = [BASE_XPROTO]
        args.target = 'django.xtarget'
        args.output = OUTPUT_DIR
        args.attic = TEST_ATTICS
        generator = XOSGenerator(args)
        output = generator.generate()
        print output
        self.assertEqual(output, DJANGO_EXPECTED_OUTPUT)

if __name__ == '__main__':
    unittest.main()