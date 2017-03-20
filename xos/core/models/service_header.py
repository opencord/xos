from core.models.xosmodel import XOS
from core.models.plcorebase import *
from django.core.validators import URLValidator
import urlparse
from operator import attrgetter
import json
from distutils.version import LooseVersion
from django.core.validators import URLValidator
from xos.exceptions import *
from xos.config import Config


COARSE_KIND = "coarse"

def get_xos():
    xos = XOS.objects.all()

    if xos:
       return xos[0]
    else:
       return None

class AttributeMixin(object):
    # helper for extracting things from a json-encoded
    # service_specific_attribute

    def get_attribute(self, name, default=None):
        if self.service_specific_attribute:
            attributes = json.loads(self.service_specific_attribute)
        else:
            attributes = {}
        return attributes.get(name, default)

    def set_attribute(self, name, value):
        if self.service_specific_attribute:
            attributes = json.loads(self.service_specific_attribute)
        else:
            attributes = {}
        attributes[name] = value
        self.service_specific_attribute = json.dumps(attributes)

    def get_initial_attribute(self, name, default=None):
        if self._initial["service_specific_attribute"]:
            attributes = json.loads(
                self._initial["service_specific_attribute"])
        else:
            attributes = {}
        return attributes.get(name, default)

    @classmethod
    def get_default_attribute(cls, name):
        for (attrname, default) in cls.simple_attributes:
            if attrname == name:
                return default
        if hasattr(cls, "default_attributes"):
            if name in cls.default_attributes:
                return cls.default_attributes[name]

        return None

    @classmethod
    def setup_simple_attributes(cls):
        for (attrname, default) in cls.simple_attributes:
            setattr(cls, attrname, property(lambda self, attrname=attrname, default=default: self.get_attribute(attrname, default),
                                            lambda self, value, attrname=attrname: self.set_attribute(
                                                attrname, value),
                                            None,
                                            attrname))

