import unittest
import os
from helpers import FakeArgs, OUTPUT_DIR
from xosgenx.generator import XOSGenerator

TEST_EXPECTED_OUTPUT = """
    name: XOSModel
    fields:
            name:
                type: string
                description: "Help Name"
            files:
                type: string
                description: "Help Files"
"""

DJANGO_EXPECTED_OUTPUT = """
from header import *from xosmodel_header import *
def top():
    return 'top'

class XOSModel(XOSBase):
  # Primitive Fields (Not Relations)
  name = StrippedCharField( help_text = "Help Name", max_length = 200, null = False, db_index = False, blank = False )
  files = StrippedCharField( help_text = "Help Files", max_length = 1024, null = False, db_index = False, blank = False )

  # Relations

  def model():
      return 'model'
  passdef bottom():
    return 'bottom'"""

BASE_XPROTO = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/xproto/base.xproto")
VROUTER_XPROTO = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/xproto/vrouterport.xproto")
TEST_TARGET = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/xtarget/test.xtarget")

TEST_ATTICS = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/attics/")

class XOSGeneratorTest(unittest.TestCase):
    """
    Testing the XOS Generative Toolchain
    """

    def setUp(self):
        filesToRemove = [f for f in os.listdir(OUTPUT_DIR)]
        for f in filesToRemove:
            if not f.startswith('.'):
                os.remove(OUTPUT_DIR + '/' + f)

    def test_generator_custom_target_from_file(self):
        """
        [XOS-GenX] Generate output from base.xproto
        """
        args = FakeArgs()
        args.files = [BASE_XPROTO]
        args.target = TEST_TARGET
        output = XOSGenerator.generate(args)
        self.assertEqual(output, TEST_EXPECTED_OUTPUT)

    def test_generator_custom_target_from_inputs(self):
        """
        [XOS-GenX] Generate output from base.xproto
        """
        args = FakeArgs()
        args.inputs = open(BASE_XPROTO).read()
        args.target = TEST_TARGET
        output = XOSGenerator.generate(args)
        self.assertEqual(output, TEST_EXPECTED_OUTPUT)

    def test_generator_tosca(self):
        """
        [XOS-GenX] Generate TOSCA from base.xproto, and write to file
        """
        args = FakeArgs()
        args.files = [BASE_XPROTO, VROUTER_XPROTO]
        args.target = 'tosca.xtarget'
        args.output = OUTPUT_DIR
        args.write_to_file = 'single'
        args.dest_file = 'base.yaml'
        XOSGenerator.generate(args)

        dest_file = OUTPUT_DIR + '/' + args.dest_file
        self.assertTrue(os.path.isfile(dest_file))

        output = open(dest_file, "r").read()
        self.assertIn("tosca.nodes.XOSModel", output)
        self.assertIn("tosca.nodes.VRouterPort", output)

    def test_django_with_attic(self):
        """
        [XOS-GenX] Generate django output from base.xproto
        """
        args = FakeArgs()
        args.files = [BASE_XPROTO]
        args.target = 'django.xtarget'
        args.output = OUTPUT_DIR
        args.attic = TEST_ATTICS
        output = XOSGenerator.generate(args)
        self.assertEqual(output, DJANGO_EXPECTED_OUTPUT)

    def test_write_multiple_files(self):
        """
        [XOS-GenX] read multiple models as input, print one file per model
        """
        args = FakeArgs()
        args.files = [BASE_XPROTO, VROUTER_XPROTO]
        args.target = TEST_TARGET
        args.output = OUTPUT_DIR
        args.dest_extension = 'txt'
        args.write_to_file = 'model'
        XOSGenerator.generate(args)

        generated_files = [f for f in os.listdir(OUTPUT_DIR) if not f.startswith('.')]
        self.assertEqual(len(generated_files), 2)

        xosmodel = open(os.path.join(OUTPUT_DIR, 'xosmodel.txt'), "r").read()
        vrouterport = open(os.path.join(OUTPUT_DIR, 'vrouterport.txt'), "r").read()

        self.assertIn("name: XOSModel", xosmodel)
        self.assertIn("name: VRouterPort", vrouterport)

if __name__ == '__main__':
    unittest.main()