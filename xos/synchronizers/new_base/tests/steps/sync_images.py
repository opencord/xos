import os
import base64
from mock_modelaccessor import *
from synchronizers.new_base.syncstep import SyncStep

class SyncImages(SyncStep):
    provides=[Image]
    requested_interval=0
    observes=[Image]

    def sync_record(self, role):
        # do nothing
        pass
