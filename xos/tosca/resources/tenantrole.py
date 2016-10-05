import os
import pdb
import sys
import tempfile

from toscaparser.tosca_template import ToscaTemplate
from core.models import User, Deployment, TenantRole
from xosresource import XOSResource

class XOSTenantRole(XOSResource):
    provides = "tosca.nodes.TenantRole"
    xos_model = TenantRole
    name_field = "role"

    def get_xos_args(self):
        args = super(XOSTenantRole, self).get_xos_args()

        return args

    def delete(self, obj):
        super(XOSTenantRole, self).delete(obj)



