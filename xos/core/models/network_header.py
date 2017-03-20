import json
import operator
from operator import attrgetter
from distutils.version import LooseVersion
from django.db import models
from django.core.validators import URLValidator
from xos.exceptions import *
import urlparse
from xos.config import Config

from core.models.plcorebase import *

# If true, then IP addresses will be allocated by the model. If false, then
# we will assume the observer handles it.
NO_OBSERVER=False
