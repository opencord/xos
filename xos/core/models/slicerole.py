

from header import *






class SliceRole(XOSBase):
  # Primitive Fields (Not Relations)
  role = StrippedCharField( blank = False, max_length = 30, null = False, db_index = False, choices = (('admin', 'Admin'), ('default', 'Default')) )
  

  # Relations
  

  def __unicode__(self):  return u'%s' % (self.role)
  pass

