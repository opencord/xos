import os
import pdb
import sys
import tempfile

from toscaparser.tosca_template import ToscaTemplate
from core.models import NodeLabel
from xosresource import XOSResource

class XOSNodeLabel(XOSResource):
    provides = "tosca.nodes.NodeLabel"
    xos_model = NodeLabel

