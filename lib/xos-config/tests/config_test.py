import unittest
import os
import config.config

basic_conf = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/confs/basic_conf.yaml')
yaml_not_valid = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/confs/yaml_not_valid.yaml')
invalid_format = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/confs/invalid_format.yaml')

class XOSConfigTest(unittest.TestCase):
    """
    Testing the XOS Config Module
    """

    def setUp(self):
        self.config = config.config.Config()

    def test_initialize_only_once(self):
        """
        [XOS-Config] Raise if initialized twice
        :return: 
        """
        with self.assertRaises(Exception) as e:
            self.config.init(basic_conf)
            self.config.init(basic_conf)
        self.assertEqual(e.exception.message, '[XOS-Config] Module already initialized')

    def test_missing_file_exception(self):
        """
        [XOS-Config] Raise if file not found 
        """
        with self.assertRaises(Exception) as e:
            self.config.init('missing_conf')
        self.assertEqual(e.exception.message, '[XOS-Config] Config file not found at: missing_conf')

    def test_yaml_not_valid(self):
        """
        [XOS-Config] Raise if yaml is not valid
        """
        with self.assertRaises(Exception) as e:
            self.config.init(yaml_not_valid)
        self.assertEqual(e.exception.message, '[XOS-Config] Config file is not a valid Yaml!')

    def test_invalid_format(self):
        """
        [XOS-Config] Raise if format is not valid (we expect a dictionary)
        """
        with self.assertRaises(Exception) as e:
            self.config.init(invalid_format)
        self.assertEqual(e.exception.message, '[XOS-Config] The config should be a dictionary')

    def test_env_override(self):
        """
        [XOS-Config] the XOS-CONFIG environment variable should override the config_file
        """
        os.environ['XOS-CONFIG'] = 'env.yaml'
        with self.assertRaises(Exception) as e:
            self.config.init('missing_conf')
        self.assertEqual(e.exception.message, '[XOS-Config] Config file not found at: env.yaml')
        del os.environ['XOS-CONFIG']

    def test_get_cli_param(self):
        args = ['-A', 'Foo', '-c', 'Bar', '-C', 'config.yaml']
        res = self.config.get_cli_param(args)
        self.assertEqual(res, 'config.yaml')

    def test_parse_basic_config(self):
        """
        [XOS-Config] Parse a simple config 
        """
        conf = self.config
        conf.init(basic_conf)
        self.assertEqual(conf.config['database']['username'], 'test')
        self.assertEqual(conf.config['database']['password'], 'safe')

