
from header import *





from core.models.controller import Controller 



from core.models.slice import Slice 






class ControllerSlice(PlCoreBase):
  # Primitive Fields (Not Relations)
  tenant_id = StrippedCharField( help_text = "Keystone tenant id", max_length = 200, null = True, db_index = False, blank = True )
  

  # Relations
  
  controller = ForeignKey(Controller, db_index = True, related_name = 'controllerslices', null = False, blank = False )
  slice = ForeignKey(Slice, db_index = True, related_name = 'controllerslices', null = False, blank = False )

  objects = ControllerLinkManager()
  deleted_objects = ControllerLinkDeletionManager()
  
  class Meta:
      unique_together = ('controller', 'slice')
   
  def tologdict(self):
      d=super(ControllerSlice,self).tologdict()
      try:
          d['slice_name']=self.slice.name
          d['controller_name']=self.controller.name
      except:
          pass
      return d
  
  def __unicode__(self):  return u'%s %s'  % (self.slice, self.controller)
  
  @staticmethod
  def select_by_user(user):
      if user.is_admin:
          qs = ControllerSlice.objects.all()
      else:
          slices = Slice.select_by_user(user)
          qs = ControllerSlice.objects.filter(slice__in=slices)
      return qs    
  
  def get_cpu_stats(self):
      filter = 'project_id=%s'%self.tenant_id
      return monitor.get_meter('cpu',filter,None)
  
  def get_bw_stats(self):
      filter = 'project_id=%s'%self.tenant_id
      return monitor.get_meter('network.outgoing.bytes',filter,None)
  
  def get_node_stats(self):
      return len(self.slice.instances)
  pass

