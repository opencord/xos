import os
import pdb
import sys
import tempfile
sys.path.append("/opt/tosca")
from translator.toscalib.tosca_template import ToscaTemplate

from core.models import DashboardView, Site, Deployment, SiteDeployment

from xosresource import XOSResource

class XOSDashboardView(XOSResource):
    provides = "tosca.nodes.DashboardView"
    xos_model = DashboardView
    copyin_props = ["url", "enabled"]

    def get_xos_args(self):
        args = super(XOSDashboardView, self).get_xos_args()
        if (self.get_property("custom_icon")):
            args["custom_icon"] = True
        return args

    def postprocess(self, obj):
        for deployment_name in self.get_requirements("tosca.relationships.SupportsDeployment"):
            deployment = self.get_xos_object(Deployment, deployment_name)
            if not deployment in obj.deployments.all():
                print "attaching dashboardview %s to deployment %s" % (obj, deployment)
                obj.deployments.add(deployment)
                obj.save()

    def can_delete(self, obj):
        return super(XOSDashboardView, self).can_delete(obj)

    def create(self):
        xos_args = self.get_xos_args()

        has_icons = xos_args.get("custom_icon", None)
        xos_args.pop("custom_icon", None)
        dashboard = DashboardView(**xos_args)

        if has_icons:
            prefix, name = dashboard.url.split(':')
            name = name[3:]
            name = name[:1].lower() + name[1:]
            dashboard.icon = "%s-icon.png" % name
            dashboard.icon_active = "%s-icon-active.png" % name

        dashboard.save()

        self.postprocess(dashboard)

        self.info("Created DashboardView '%s'" % (str(dashboard), ))
