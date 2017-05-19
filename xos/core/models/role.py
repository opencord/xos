

from header import *






class Role(XOSBase):
  # Primitive Fields (Not Relations)
  role_type = StrippedCharField( db_index = False, max_length = 80, null = False, blank = False )
  role = StrippedCharField( db_index = False, max_length = 80, null = True, blank = True )
  description = StrippedCharField( db_index = False, max_length = 120, null = False, blank = False )
  content_type = StrippedCharField( help_text = "Content type id linked to this role", max_length = 1024, null = False, db_index = False, blank = False )
  

  # Relations
  

  def __unicode__(self):  return u'%s:%s' % (self.content_type,self.role_type)
  pass

