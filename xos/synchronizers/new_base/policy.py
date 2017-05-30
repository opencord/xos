import os
import base64
from xos.config import Config
from xos.logger import Logger, logging
from synchronizers.new_base.modelaccessor import *
from synchronizers.new_base.ansible_helper import run_template
#from synchronizers.new_base.steps import *
#from synchronizers.new_base.ansible_helper import *
#from generate.dependency_walker import *

import json
import time
import pdb

logger = Logger(level=logging.DEBUG)

class Policy(object):
    """ An XOS Model Policy """
    def __init__(self):
        pass

