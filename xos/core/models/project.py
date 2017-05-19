

from header import *






class Project(XOSBase):
  # Primitive Fields (Not Relations)
  name = StrippedCharField( help_text = "Name of Project", max_length = 200, null = False, db_index = False, blank = False )
  

  # Relations
  

  def __unicode__(self):  return u'%s' % (self.name)
  pass

