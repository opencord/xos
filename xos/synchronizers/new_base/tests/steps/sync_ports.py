import os
import base64
from mock_modelaccessor import *
from synchronizers.new_base.syncstep import SyncStep

class SyncPort(SyncStep):
    requested_interval = 0 # 3600
    provides=[Port]
    observes=Port

    def call(self, failed=[], deletion=False):
        if deletion:
            self.delete_ports()
        else:
            self.sync_ports()

    def sync_ports(self):
        open('/tmp/sync_ports','w').write('Sync successful')
        

    def delete_ports(self):
        open('/tmp/delete_ports','w').write('Delete successful')
