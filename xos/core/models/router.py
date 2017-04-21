
from header import *





from core.models.slice import Slice 



from core.models.network import Network 



from core.models.network import Network 






class Router(PlCoreBase):
  # Primitive Fields (Not Relations)
  name = CharField( blank = False, max_length = 32, null = False, db_index = False )
  

  # Relations
  
  owner = ForeignKey(Slice, db_index = True, related_name = 'routers', null = False, blank = False )
  permittedNetworks = ManyToManyField(Network, db_index = False, related_name = 'availableRouters', null = False, through = 'Router_permittedNetworks', blank = True )
  networks = ManyToManyField(Network, db_index = False, related_name = 'routers', null = False, through = 'Router_networks', blank = True )

  def __unicode__(self):  return u'%s' % (self.name)
  
  def can_update(self, user):
      return user.can_update_slice(self.owner)
  
  pass

