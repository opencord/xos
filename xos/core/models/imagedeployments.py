
from header import *





from core.models.image import Image 



from core.models.deployment import Deployment 






class ImageDeployments(PlCoreBase):
  # Primitive Fields (Not Relations)
  

  # Relations
  
  image = ForeignKey(Image, db_index = True, related_name = 'imagedeployments', null = False, blank = False )
  deployment = ForeignKey(Deployment, db_index = True, related_name = 'imagedeployments', null = False, blank = False )

  class Meta:
      unique_together = ('image', 'deployment')
  
  def __unicode__(self):  return u'%s %s' % (self.image, self.deployment)
  
  def can_update(self, user):
      return user.can_update_deployment(self.deployment)
  pass

