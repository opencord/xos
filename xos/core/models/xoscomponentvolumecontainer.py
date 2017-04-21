
from header import *





from core.models.xoscomponent import XOSComponent 






class XOSComponentVolumeContainer(PlCoreBase):
  # Primitive Fields (Not Relations)
  name = StrippedCharField( help_text = "Volume Name", max_length = 300, null = False, db_index = False, blank = False )
  container = StrippedCharField( help_text = "Volume Name", max_length = 300, null = False, db_index = False, blank = False )
  

  # Relations
  
  component = ForeignKey(XOSComponent, help_text = "The Component object for this VolumeContainer", related_name = 'volumecontainers', null = False, db_index = True, blank = False )

  def save(self, *args, **kwds):
      # If this is a new object, then check to make sure it doesn't already exist
      if not self.pk:
          existing = XOSComponentVolumeContainer.objects.filter(name=self.name)
          if len(existing) > 0:
              raise XOSValidationError('XOSComponentVolumeContainer for %s:%s already defined' % (self.container_path, self.host_path))
      super(XOSComponentVolumeContainer, self).save(*args, **kwds)
  
  pass

