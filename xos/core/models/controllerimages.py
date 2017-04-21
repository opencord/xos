
from header import *





from core.models.image import Image 



from core.models.controller import Controller 






class ControllerImages(PlCoreBase):
  # Primitive Fields (Not Relations)
  glance_image_id = StrippedCharField( help_text = "Glance image id", max_length = 200, null = True, db_index = False, blank = True )
  

  # Relations
  
  image = ForeignKey(Image, db_index = True, related_name = 'controllerimages', null = False, blank = False )
  controller = ForeignKey(Controller, db_index = True, related_name = 'controllerimages', null = False, blank = False )

  class Meta:
      unique_together = ('image', 'controller')
           
  def __unicode__(self):  return u'%s %s' % (self.image, self.controller)
  
  objects = ControllerLinkManager()
  deleted_objects = ControllerLinkDeletionManager()
  pass

