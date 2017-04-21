
from header import *





from core.models.contenttype import ContentType 






class Role(PlCoreBase):
  # Primitive Fields (Not Relations)
  role_type = StrippedCharField( db_index = False, max_length = 80, null = False, blank = False )
  role = StrippedCharField( db_index = False, max_length = 80, null = True, blank = True )
  description = StrippedCharField( db_index = False, max_length = 120, null = False, blank = False )
  

  # Relations
  
  content_type = ForeignKey(ContentType, db_index = True, related_name = 'role', null = False, blank = False )

  def __unicode__(self):  return u'%s:%s' % (self.content_type,self.role_type)
  pass

