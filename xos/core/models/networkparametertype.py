

from header import *






class NetworkParameterType(XOSBase):
  # Primitive Fields (Not Relations)
  name = CharField( help_text = "The name of this parameter", max_length = 128, null = False, db_index = True, blank = False )
  description = CharField( blank = False, max_length = 1024, null = False, db_index = False )
  

  # Relations
  

  def __unicode__(self):  return u'%s' % (self.name)
  pass

