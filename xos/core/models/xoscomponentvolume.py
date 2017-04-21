
from header import *





from core.models.xoscomponent import XOSComponent 






class XOSComponentVolume(PlCoreBase):
  # Primitive Fields (Not Relations)
  name = StrippedCharField( help_text = "Volume Name", max_length = 300, null = False, db_index = False, blank = False )
  container_path = StrippedCharField( help_text = "Path of Volume in Container", max_length = 1024, null = False, db_index = False, blank = False )
  host_path = StrippedCharField( help_text = "Path of Volume in Host", max_length = 1024, null = False, db_index = False, blank = False )
  read_only = BooleanField( default = False, help_text = "True if mount read-only", null = False, db_index = False, blank = True )
  

  # Relations
  
  component = ForeignKey(XOSComponent, help_text = "The Component object for this Volume", related_name = 'volumes', null = False, db_index = True, blank = False )

  def save(self, *args, **kwds):
      # If this is a new object, then check to make sure it doesn't already exist
      if not self.pk:
          existing = XOSComponentVolume.objects.filter(container_path=self.container_path, host_path=self.host_path)
          if len(existing) > 0:
              raise XOSValidationError('XOSComponentVolume for %s:%s already defined' % (self.container_path, self.host_path))
      super(XOSComponentVolume, self).save(*args, **kwds)
  
  pass

