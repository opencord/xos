import os
import unittest

from xosutil import autodiscover_version

test_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

class XOSUtilTest(unittest.TestCase):
    """
    Testing the XOS Util Module
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_autodiscover_version_of_caller(self):
        version = open(os.path.join(test_path, "../../../VERSION")).readline().strip()
        self.assertEqual(version, autodiscover_version.autodiscover_version_of_caller())

    def test_autodiscover_version_of_caller_save_to(self):
        version = open(os.path.join(test_path, "../../../VERSION")).readline().strip()
        test_save_fn = os.path.join(test_path, "test_version.py")
        if os.path.exists(test_save_fn):
            os.remove(test_save_fn)
        self.assertEqual(version, autodiscover_version.autodiscover_version_of_caller(save_to="test_version.py"))
        self.assertTrue(os.path.exists(test_save_fn))
        self.assertTrue(version in open(test_save_fn).read())

if __name__ == "__main__":
    unittest.main()
