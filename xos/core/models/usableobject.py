
from header import *








class UsableObject(PlCoreBase):
  # Primitive Fields (Not Relations)
  name = StrippedCharField( db_index = False, max_length = 1024, null = False, blank = False )
  

  # Relations
  

  def __unicode__(self):  return u'%s' % (self.name)
  pass

