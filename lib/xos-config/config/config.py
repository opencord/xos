import os
import sys
import yaml
import requests
import default

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
        """
        Read a parameter from the config
        :param query: a dot separated selector for configuration options (eg: database.username)
        :return: the requested parameter in any format the parameter is specified
        """
        val = self.get_param(query, self.config)
        if not val:
            val = self.get_param(query, default.DEFAULT_VALUES)
        if not val:
            raise Exception('[XOS-Config] Config does not have a value (or a default) parameter %s' % query)
        return val

    def get_param(self, query, config):
        """
        Search for a parameter in config's first level, other call get_nested_param
        :param query: a dot separated selector for configuration options (eg: database.username)
        :param config: the config source to read from (can be the config file or the defaults)
        :return: the requested parameter in any format the parameter is specified
        """
        keys = query.split('.')
        if len(keys) == 1:
            key = keys[0]
            if not config.has_key(key):
                return None
            return config[key]
        else:
            return self.get_nested_param(keys, config)

    def get_nested_param(self, keys, config):
        """
        
        :param keys: a list of descending selector
        :param config: the config source to read from (can be the config file or the defaults)
        :return: the requested parameter in any format the parameter is specified
        """
        param = config
        for k in keys:
            if not param.has_key(k):
                return None
            param = param[k]
        return param

    def get_service_list(self):
        """
        Query registrator to get the list of services
        NOTE: we assume that consul is a valid URL
        :return: a list of service names 
        """
        service_dict = requests.get('http://consul:8500/v1/catalog/services').json()
        service_list = []
        for s in service_dict:
            service_list.append(s)
        return service_list

    def get_service_info(self, service_name):
        """
        Query registrator to get the details about a service
        NOTE: we assume that consul is a valid URL
        :param service_name: the name of the service, can be retrieved from get_service_list
        :return: the informations about a service
        """
        response = requests.get('http://consul:8500/v1/catalog/service/%s' % service_name)
        if not response.ok:
            raise Exception('[XOS-Config] Registrator is down')
        service = response.json()
        if not service or len(service) == 0:
            raise Exception('[XOS-Config] The service missing-service looking for does not exist')
        return {
            'name': service[0]['ServiceName'],
            'url': service[0]['ServiceAddress'],
            'port': service[0]['ServicePort']
        }

    def getServiceEndpoint(self, service_name):
        """
        Query registrator to get the details about a service and return the endpoint in for of a string
        :param service_name: the name of the service, can be retrieved from get_service_list
        :return: the endpoint of the service
        """
        service = self.get_service_info(service_name)
        return 'http://%s:%s' % (service['url'], service['port'])

    # TODO
    # [ ] Validate Logging

# NOTE is this needed if this package is not meant to be execute from the CLI?
if __name__ == '__main__':
    config = Config()
    config.init()