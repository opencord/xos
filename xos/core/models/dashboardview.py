
from header import *





from core.models.controller import Controller 



from core.models.deployment import Deployment 






class DashboardView(PlCoreBase):
  # Primitive Fields (Not Relations)
  name = StrippedCharField( help_text = "Name of the View", max_length = 200, null = False, db_index = False, blank = False )
  url = StrippedCharField( help_text = "URL of Dashboard", max_length = 1024, null = False, db_index = False, blank = False )
  enabled = BooleanField( default = True, null = False, blank = True, db_index = False )
  icon = CharField( default = "default-icon.png", max_length = 200, blank = False, help_text = "Icon for Dashboard", null = False, db_index = False )
  icon_active = CharField( default = "default-icon-active.png", max_length = 200, blank = False, help_text = "Icon for active Dashboard", null = False, db_index = False )
  

  # Relations
  
  controllers = ManyToManyField(Controller, db_index = False, related_name = 'dashboardviews', null = False, through = 'ControllerDashboardView', blank = True )
  deployments = ManyToManyField(Deployment, related_name = 'dashboardviews', through = 'DashboardView_deployments', blank = True, help_text = "Deployments that should be included in this view", null = False, db_index = False )

  def __unicode__(self): return u'%s' % (self.name)
  pass

