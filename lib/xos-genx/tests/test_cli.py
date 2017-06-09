import unittest
import os
from mock import patch
from xosgenx.xosgen import XosGen

class Args:
    pass

class XOSGeneratorTest(unittest.TestCase):
    """
    Testing the CLI binding for the XOS Generative Toolchain
    """

    def test_generator(self):
        """
        [XOS-GenX] The CLI entry point should correctly parse params
        """
        args = Args()
        args.files = ['../test.xproto']
        args.target = '../test.xtarget'
        args.output = '../out/dir/'

        expected_args = Args()
        expected_args.files = [os.path.abspath(os.getcwd() + '/' + args.files[0])]
        expected_args.target = os.path.abspath(os.getcwd() + '/' + args.target)
        expected_args.output = os.path.abspath(os.getcwd() + '/' + args.output)

        with patch("xosgenx.xosgen.XOSGenerator.generate") as generator:
            XosGen.init(args)
            actual_args = generator.call_args[0][0]
            self.assertEqual(actual_args.files, expected_args.files)
            self.assertEqual(actual_args.target, expected_args.target)
            self.assertEqual(actual_args.output, expected_args.output)

if __name__ == '__main__':
    unittest.main()