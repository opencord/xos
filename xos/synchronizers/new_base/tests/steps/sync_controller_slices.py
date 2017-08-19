import os
import base64
import syncstep
from synchronizers.new_base.ansible_helper import *
from mock_modelaccessor import *

class SyncControllerSlices(syncstep.SyncStep):
    provides=[Slice]
    requested_interval=0
    observes=ControllerSlice
    playbook='sync_controller_slices.yaml'

    def map_sync_inputs(self, controller_slice):
        if getattr(controller_slice, 'force_fail',None):
            raise Exception("Forced failure")
        elif getattr(controller_slice, 'force_defer', None):
            raise syncstep.DeferredException("Forced defer")

        tenant_fields = {'endpoint': 'endpoint',
                         'name':'Flagrant Haircut'
                         }

        return tenant_fields

    def map_sync_outputs(self, controller_slice, res):
        controller_slice.save()


    def map_delete_inputs(self, controller_slice):
        tenant_fields = {'endpoint': 'endpoint',
                          'name':'Conscientious Plastic',
                          'delete': True}
	return tenant_fields
