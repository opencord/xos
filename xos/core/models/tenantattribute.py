

from header import *
from service_header import *
 


from core.models.tenant import Tenant 






class TenantAttribute(XOSBase):
  # Primitive Fields (Not Relations)
  name = CharField( help_text = "Attribute Name", max_length = 128, null = False, db_index = False, blank = False )
  value = TextField( help_text = "Attribute Value", null = False, blank = False, db_index = False )
  

  # Relations
  
  tenant = ForeignKey(Tenant, help_text = "The Tenant this attribute is associated with", related_name = 'tenantattributes', null = False, db_index = True, blank = False )

  def __unicode__(self): return u'%s-%s' % (self.name, self.id)
  pass

