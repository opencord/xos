import unittest
import os
from mock import patch
from xosgen.xosgen import XosGen

class Args:
    pass

class XOSGeneratorTest(unittest.TestCase):
    """
    Testing the CLI binding for the XOS Generative Toolchain
    """

    def _test_generator(self):
        """
        [XOS-GenX] The CLI entry point should correctly parse params  
        """
        args = Args()
        args.inputs = ['../test.xproto']
        args.target = '../test.xtarget'
        args.output = '../out/dir/'

        expected_args = Args()
        expected_args.inputs = [os.path.abspath(os.getcwd() + '/' + args.inputs[0])]
        expected_args.target = os.path.abspath(os.getcwd() + '/' + args.target)
        expected_args.output = os.path.abspath(os.getcwd() + '/' + args.output)

        with patch("xosgen.xosgen.XOSGenerator") as generator:
            XosGen.init(args)
            generator.assert_called_with(expected_args)

if __name__ == '__main__':
    unittest.main()
