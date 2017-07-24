from core.models.plcorebase import *
from django.db.models import *



from core.models import Service

from core.models import Tenant

class MonitoringPublisher_decl(Tenant):

  KIND = "monitoring"

  class Meta:
      app_label = "monitoring"
      # name = Set a name in your xproto!
      verbose_name = "A-CORD Monitoring Service"

  # Primitive Fields (Not Relations)


  # Relations


  pass
