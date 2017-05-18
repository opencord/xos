import unittest
from mock import Mock, patch
import os
import config.config

basic_conf = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/confs/basic_conf.yaml')
yaml_not_valid = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/confs/yaml_not_valid.yaml')
invalid_format = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/confs/invalid_format.yaml')
test_conf = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/confs/test_conf.yaml')

services_list = {
  "xos-ws": [],
  "xos-db": [],
}

db_service = [
          {
            "ModifyIndex": 6,
            "CreateIndex": 6,
            "Node": "0152982c3159",
            "Address": "172.19.0.2",
            "ServiceID": "0d53ce210785:frontend_xos_db_1:5432",
            "ServiceName": "xos-db",
            "ServiceTags": [],
            "ServiceAddress": "172.18.0.4",
            "ServicePort": 5432,
            "ServiceEnableTagOverride": "false"
          }
        ]

class XOSConfigTest(unittest.TestCase):
    """
    Testing the XOS Config Module
    """

    def setUp(self):
        self.config = config.config.Config()

    def test_initialize_only_once(self):
        """
        [XOS-Config] Raise if initialized twice
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
        """
        [XOS-Config] Should read CLI -C param
        """
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

    def test_get_default_val_for_missing_param(self):
        """
        [XOS-Config] Should raise reading a missing param
        """
        self.config.init(basic_conf)
        log = self.config.get('logging')
        self.assertEqual(log, {
            'level': 'info',
            'channels': ['file', 'console']
        })

    def test_get_missing_param(self):
        """
        [XOS-Config] Should raise reading a missing param
        """
        self.config.init(test_conf)
        with self.assertRaises(Exception) as e:
            self.config.get('foo')
        self.assertEqual(e.exception.message, '[XOS-Config] Config does not have a value (or a default) parameter foo')

    def test_get_first_level(self):
        """
        [XOS-Config] Should return a first level param
        """
        self.config.init(test_conf)
        res = self.config.get('database')
        self.assertEqual(res, {
            'username': 'test',
            'password': 'safe'
        })

    def test_get_child_level(self):
        """
        [XOS-Config] Should return a child level param
        """
        self.config.init(test_conf)
        res = self.config.get('nested.parameter.for')
        self.assertEqual(res, 'testing')

    def test_get_service_list(self):
        """
        [XOS-Config] Should query registrator and return a list of services
        """
        with patch('config.config.requests.get') as mock_get:
            mock_get.return_value.json.return_value = services_list
            self.config.init(test_conf)
            res = self.config.get_service_list()
            self.assertEqual(res, [
                'xos-ws',
                'xos-db',
            ])

    def test_get_service_info(self):
        """
        [XOS-Config] Should query registrator and return service info
        """
        with patch('config.config.requests.get') as mock_get:
            mock_get.return_value.json.return_value = db_service
            self.config.init(test_conf)
            info = self.config.get_service_info('xos-db')
            self.assertEqual(info, {
                'name': 'xos-db',
                'url': '172.18.0.4',
                'port': 5432
            })

    def test_fail_get_service_info(self):
        """
        [XOS-Config] Should query registrator and return an exception if it's down
        """
        with patch('config.config.requests.get') as mock_get:
            mock_get.return_value.ok = False
            self.config.init(test_conf)
            with self.assertRaises(Exception) as e:
                self.config.get_service_info('missing-service')
            self.assertEqual(e.exception.message, '[XOS-Config] Registrator is down')

    def test_missing_get_service_info(self):
        """
        [XOS-Config] Should query registrator and return an exception if service is not there
        """
        with patch('config.config.requests.get') as mock_get:
            mock_get.return_value.json.return_value = []
            self.config.init(test_conf)
            with self.assertRaises(Exception) as e:
                self.config.get_service_info('missing-service')
            self.assertEqual(e.exception.message, '[XOS-Config] The service missing-service looking for does not exist')


    def test_get_service_endpoint(self):
        """
        [XOS-Config] Should query registrator and return service endpoint
        """
        with patch('config.config.requests.get') as mock_get:
            mock_get.return_value.json.return_value = db_service
            self.config.init(test_conf)
            endpoint = self.config.getServiceEndpoint('xos-db')
            self.assertEqual(endpoint, 'http://172.18.0.4:5432')