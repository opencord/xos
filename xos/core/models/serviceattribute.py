
from header import *

from service_header import *



from core.models.service import Service 






class ServiceAttribute(PlCoreBase):
  # Primitive Fields (Not Relations)
  name = CharField( help_text = "Attribute Name", max_length = 128, null = False, db_index = False, blank = False )
  value = TextField( help_text = "Attribute Value", null = False, blank = False, db_index = False )
  

  # Relations
  
  service = ForeignKey(Service, help_text = "The Service this attribute is associated with", related_name = 'serviceattributes', null = False, db_index = True, blank = False )

  
  pass

