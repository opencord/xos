
from header import *





from core.models.network import Network 



from core.models.controller import Controller 






class ControllerNetwork(PlCoreBase):
  # Primitive Fields (Not Relations)
  subnet = CharField( blank = True, max_length = 32, null = False, db_index = False )
  start_ip = CharField( blank = True, max_length = 32, null = False, db_index = False )
  stop_ip = CharField( blank = True, max_length = 32, null = False, db_index = False )
  net_id = CharField( help_text = "Neutron network", max_length = 256, null = True, db_index = False, blank = True )
  router_id = CharField( help_text = "Neutron router id", max_length = 256, null = True, db_index = False, blank = True )
  subnet_id = CharField( help_text = "Neutron subnet id", max_length = 256, null = True, db_index = False, blank = True )
  gateway = CharField( blank = True, max_length = 32, null = True, db_index = False )
  segmentation_id = CharField( blank = True, max_length = 32, null = True, db_index = False )
  

  # Relations
  
  network = ForeignKey(Network, db_index = True, related_name = 'controllernetworks', null = False, blank = False )
  controller = ForeignKey(Controller, db_index = True, related_name = 'controllernetworks', null = False, blank = False )

  class Meta:
      unique_together = ('network', 'controller')
  
  def tologdict(self):
      d=super(ControllerNetwork,self).tologdict()
      try:
          d['network_name']=self.network.name
          d['controller_name']=self.controller.name
      except:
          pass
      return d
  
  @staticmethod
  def select_by_user(user):
      if user.is_admin:
          qs = ControllerNetwork.objects.all()
      else:
          from core.models.slice import Slice
          slices = Slice.select_by_user(user)
          networks = Network.objects.filter(owner__in=slices)
          qs = ControllerNetwork.objects.filter(network__in=networks)
      return qs
  
  pass

