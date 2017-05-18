import os
import yaml

class Config:
    """
    XOS Configuration APIs
    """
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.read_config(config_file)

    def read_config(self, config_file):

        if not os.path.exists(config_file):
            raise Exception('[XOS-Config] Config file not found')

        with open(config_file, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                raise Exception('[XOS-Config] Config file not valid')
