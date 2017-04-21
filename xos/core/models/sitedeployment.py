
from header import *





from core.models.site import Site 



from core.models.deployment import Deployment 



from core.models.controller import Controller 






class SiteDeployment(PlCoreBase):
  # Primitive Fields (Not Relations)
  availability_zone = StrippedCharField( help_text = "OpenStack availability zone", max_length = 200, null = True, db_index = False, blank = True )
  

  # Relations
  
  site = ForeignKey(Site, db_index = True, related_name = 'sitedeployments', null = False, blank = False )
  deployment = ForeignKey(Deployment, db_index = True, related_name = 'sitedeployments', null = False, blank = False )
  controller = ForeignKey(Controller, db_index = True, related_name = 'sitedeployments', null = True, blank = True )

  objects = ControllerLinkManager()
  deleted_objects = ControllerLinkDeletionManager()
  
  class Meta:
      unique_together = ('site', 'deployment', 'controller')
  
  def __unicode__(self):  return u'%s %s' % (self.deployment, self.site)
  pass

