import os
import yaml

# NOTE is there any better approach than an hardcoded path?
DEFAULT_CONFIG = "/opt/xos/config.yaml"

class Config:
    """
    XOS Configuration APIs
    """
    def __init__(self, config_file):
        if config_file:
            self.config_file = config_file
        else:
            self.config_file = DEFAULT_CONFIG
        self.config = self.read_config(self.config_file)

    def validate_config_format(self, config):
        if not isinstance(config, dict):
            raise Exception('[XOS-Config] The config should be a dictionary')
        return config

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
