

from header import *



from core.models.controller import Controller 



from core.models.dashboardview import DashboardView 






class ControllerDashboardView(XOSBase):
  # Primitive Fields (Not Relations)
  enabled = BooleanField( default = True, null = False, blank = True, db_index = False )
  url = StrippedCharField( help_text = "URL of Dashboard", max_length = 1024, null = False, db_index = False, blank = False )
  

  # Relations
  
  controller = ForeignKey(Controller, db_index = True, related_name = 'controllerdashboardviews', null = False, blank = False )
  dashboardView = ForeignKey(DashboardView, db_index = True, related_name = 'controllerdashboardviews', null = False, blank = False )

  objects = ControllerLinkManager()
  deleted_objects = ControllerLinkDeletionManager()
  pass

