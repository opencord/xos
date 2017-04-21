
from header import *








class DeploymentRole(PlCoreBase):
  # Primitive Fields (Not Relations)
  role = StrippedCharField( blank = False, max_length = 30, null = False, db_index = False, choices = (('admin', 'Admin'),) )

  def __unicode__(self):  return u'%s' % (self.role)
