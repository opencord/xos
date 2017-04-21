
from header import *

from service_header import *



from core.models.service import Service 






class ServiceMonitoringAgentInfo(PlCoreBase):
  # Primitive Fields (Not Relations)
  name = CharField( help_text = "Monitoring Agent Name", max_length = 128, null = False, db_index = False, blank = False )
  target_uri = TextField( help_text = "Monitoring collector URI to be used by agents to publish the data", null = False, blank = False, db_index = False )
  

  # Relations
  
  service = ForeignKey(Service, help_text = "The Service this attribute is associated with", related_name = 'servicemonitoringagents', null = True, db_index = True, blank = True )

  
  pass

