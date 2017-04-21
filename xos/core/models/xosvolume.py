
from header import *





from core.models.xos import XOS 






class XOSVolume(PlCoreBase):
  # Primitive Fields (Not Relations)
  container_path = StrippedCharField( help_text = "Path of Volume in Container", max_length = 1024, null = False, db_index = False, blank = False )
  host_path = StrippedCharField( help_text = "Path of Volume in Host", max_length = 1024, null = False, db_index = False, blank = False )
  read_only = BooleanField( default = False, help_text = "True if mount read-only", null = False, db_index = False, blank = True )
  

  # Relations
  
  xos = ForeignKey(XOS, help_text = "The XOS object for this Volume", related_name = 'volumes', null = False, db_index = True, blank = False )

  def __unicode__(self): return u'%s' % (self.container_path)
  
  def save(self, *args, **kwargs):
     super(XOSVolume, self).save(*args, **kwargs)
  
     # This is necessary, as the XOS syncstep handles rerunning the docker-
     # compose.
     # TODO: Update onboarding synchronizer and replace this with watcher functionality
     if self.xos:
         # force XOS to rebuild
         self.xos.save(update_fields=["updated"])
  pass

