import unittest
import os
import config.config

basic_conf = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/confs/basic_conf.yaml')

class XOSConfigTest(unittest.TestCase):
    """
    Testing the XOS Config Module
    """

    def test_missing_file_exception(self):
        """
        [XOS-Config] Raise if file not found 
        """
        with self.assertRaises(Exception):
            config.config.Config('missing_conf')

    def test_parse_basic_config(self):
        """
        [XOS-Config] Parse a simple config 
        """
        conf = config.config.Config(basic_conf)
        self.assertEqual(conf.config['database']['username'], 'test')
