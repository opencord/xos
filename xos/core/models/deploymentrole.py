

from header import *






class DeploymentRole(XOSBase):
  # Primitive Fields (Not Relations)
  role = StrippedCharField( blank = False, max_length = 30, null = False, db_index = False, choices = (('admin', 'Admin'),) )
  

  # Relations
  

  def __unicode__(self): return u'%s' % (self.role)
  pass

