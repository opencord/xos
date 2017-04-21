
from header import *


from service_header import *
 





class TenantRootRole(PlCoreBase):
  # Primitive Fields (Not Relations)
  role = StrippedCharField( blank = False, max_length = 30, null = False, db_index = False, choices = (('admin', 'Admin'), ('access', 'Access')) )
  

  # Relations
  

  def __unicode__(self): return u'%s' % (self.role)
  pass

