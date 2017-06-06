import unittest
import os
from xosgen.generator import XOSGenerator

XPROTO_FILE = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/test_xproto/base.xproto")

class Args:
    pass

class XOSGenXTest(unittest.TestCase):
    """
    Testing the XOS Generative Toolchain
    """

    def test_read_input_files(self):
        """
        [XOS-GenX] Get a list of file names and read them  
        """
        args = Args()
        args.inputs = [XPROTO_FILE]
        generator = XOSGenerator(args)
        res = generator._read_input_files(args.inputs)
        self.assertEqual(res, """message XOSModel (XOSBase) {
     required string name = 1 [max_length = 200, content_type = "stripped", blank = False, help_text = "Help Name", null = False, db_index = False];
     required string files = 2 [max_length = 1024, content_type = "stripped", blank = False, help_text = "Help Files", null = False, db_index = False];
}""")

    def test_get_template(self):
        """
        [XOS-GenX] Should transform relative path to absolute path  
        """
        args = Args()
        generator = XOSGenerator(args)
        res = generator._get_template('sample.xtarget')
        self.assertEqual(res, os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../sample.xtarget"))

        generator = XOSGenerator(args)
        res = generator._get_template('/sample.xtarget')
        self.assertEqual(res, "/sample.xtarget")
