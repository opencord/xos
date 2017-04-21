
from header import *





from core.models.deployment import Deployment 






class Image(PlCoreBase):
  # Primitive Fields (Not Relations)
  name = StrippedCharField( db_index = False, max_length = 256, null = False, blank = False )
  kind = CharField( default = "vm", choices = (('vm', 'Virtual Machine'), ('container', 'Container')), max_length = 30, blank = False, null = False, db_index = False )
  disk_format = StrippedCharField( db_index = False, max_length = 256, null = False, blank = False )
  container_format = StrippedCharField( db_index = False, max_length = 256, null = False, blank = False )
  path = StrippedCharField( help_text = "Path to image on local disk", max_length = 256, null = True, db_index = False, blank = True )
  tag = StrippedCharField( help_text = "For Docker Images, tag of image", max_length = 256, null = True, db_index = False, blank = True )
  

  # Relations
  
  deployments = ManyToManyField(Deployment, help_text = "Select which images should be instantiated on this deployment", related_name = 'images', null = False, db_index = False, blank = True )

  objects = ControllerLinkManager()
  deleted_objects = ControllerLinkDeletionManager()
  
  def __unicode__(self):  return u'%s' % (self.name)
  pass

