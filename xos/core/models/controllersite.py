
from header import *





from core.models.site import Site 



from core.models.controller import Controller 






class ControllerSite(PlCoreBase):
  # Primitive Fields (Not Relations)
  tenant_id = StrippedCharField( help_text = "Keystone tenant id", max_length = 200, null = True, db_index = True, blank = True )
  

  # Relations
  
  site = ForeignKey(Site, db_index = True, related_name = 'controllersite', null = False, blank = False )
  controller = ForeignKey(Controller, db_index = True, related_name = 'controllersite', null = True, blank = True )

  class Meta:
      unique_together = ('site', 'controller')
  pass

