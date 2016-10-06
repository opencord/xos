import os
import pdb
import sys
import tempfile
sys.path.append("/opt/tosca")
from translator.toscalib.tosca_template import ToscaTemplate

from core.models import LoadableModule, LoadableModuleResource, Library

from loadablemodule import XOSLoadableModule

# This is like ServiceController, but with the synchronizer stuff removed

class XOSLibrary(XOSLoadableModule):
    provides = "tosca.nodes.Library"
    xos_model = Library
    copyin_props = ["version", "provides", "requires", "base_url"]

    def postprocess(self, obj):
        super(XOSLibrary, self).postprocess(obj)



