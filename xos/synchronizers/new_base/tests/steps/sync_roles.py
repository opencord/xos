import os
import base64
from mock_modelaccessor import *
import syncstep 

class SyncRoles(syncstep.SyncStep):
    provides=[Role]
    requested_interval=0
    observes=[SiteRole,SliceRole,ControllerRole]

    def sync_record(self, role):
        if not role.enacted:
            controllers = Controller.objects.all()
       	    for controller in controllers:
                driver = self.driver.admin_driver(controller=controller)
                driver.create_role(role.role)
            role.save()
    
