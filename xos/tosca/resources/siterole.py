import os
import pdb
import sys
import tempfile

from toscaparser.tosca_template import ToscaTemplate
from core.models import User, Deployment, SiteRole
from xosresource import XOSResource

class XOSSiteRole(XOSResource):
    provides = "tosca.nodes.SiteRole"
    xos_model = SiteRole
    name_field = "role"

    def get_xos_args(self):
        args = super(XOSSiteRole, self).get_xos_args()

        return args

    def delete(self, obj):
        super(XOSSiteRole, self).delete(obj)



