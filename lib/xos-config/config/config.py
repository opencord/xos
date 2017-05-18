import os
import sys
import yaml
import requests
import json

# NOTE is there any better approach than an hardcoded path?
DEFAULT_CONFIG = "/opt/xos/config.yaml"

class Config:
    """
    XOS Configuration APIs
    """
    def __init__(self):
        self.initialized = False

    def init(self, config_file=DEFAULT_CONFIG):

        # the config module can be initialized only one
        if self.initialized:
            raise Exception('[XOS-Config] Module already initialized')
        self.initialized = True

        # if XOS-CONFIG is defined override the config_file
        if os.environ.get('XOS-CONFIG'):
            config_file = os.environ['XOS-CONFIG']

        # if a -C parameter is set in the cli override the config_file
        # FIXME shouldn't this stay in whatever module call this one? and then just pass the file to the init method
        if self.get_cli_param(sys.argv):
            config_file = self.get_cli_param(sys.argv)

        self.config = self.read_config(config_file)

    @staticmethod
    def validate_config_format(config):
        if not isinstance(config, dict):
            raise Exception('[XOS-Config] The config should be a dictionary')
        return config

    @staticmethod
    def get_cli_param(args):
        last = None
        for arg in args:
            if last == '-C':
                return arg
            last = arg

    def read_config(self, config_file):
        """
        Read the configuration file and return a dictionary
        :param config_file: string
        :return: dict
        """
        if not os.path.exists(config_file):
            raise Exception('[XOS-Config] Config file not found at: %s' % config_file)

        with open(config_file, 'r') as stream:
            try:
                return self.validate_config_format(yaml.safe_load(stream))
            except yaml.YAMLError as exc:
                raise Exception('[XOS-Config] Config file is not a valid Yaml!')

    def get(self, query):
        keys = query.split('.')
        if len(keys) == 1:
            key = keys[0]
            if not self.config.has_key(key):
                raise Exception('[XOS-Config] Config does not have parameter %s' % query)
            return self.config[key]
        else:
            param = self.config
            for k in keys:
                if not param.has_key(k):
                    raise Exception('[XOS-Config] Config does not have parameter %s' % query)
                param = param[k]
            return param

    def getServiceInfo(self, service_name):
        response = requests.get('http://consul:8500/v1/catalog/service/%s' % service_name)
        service = response.json()[0]
        return {
            'name': service['ServiceName'],
            'url': service['ServiceAddress'],
            'port': service['ServicePort']
        }

    def getServiceEndpoint(self, service_name):
        service = self.getServiceInfo(service_name)
        return 'http://%s:%s' % (service['url'], service['port'])

    # TODO
    # [ ] List services
    # [ ] Raise if service does not exist
    # [ ] Validate Loggin

# NOTE is this needed if this package is not meant to be execute from the CLI?
if __name__ == '__main__':
    config = Config()
    config.init()