
from header import *





from core.models.deployment import Deployment 






class Flavor(PlCoreBase):
  # Primitive Fields (Not Relations)
  name = StrippedCharField( help_text = "name of this flavor, as displayed to users", max_length = 32, null = False, db_index = False, blank = False )
  description = StrippedCharField( db_index = False, max_length = 1024, null = True, blank = True )
  flavor = StrippedCharField( help_text = "flavor string used to configure deployments", max_length = 32, null = False, db_index = False, blank = False )
  order = IntegerField( default = 0, help_text = "used to order flavors when displayed in a list", null = False, db_index = False, blank = False )
  default = BooleanField( default = False, help_text = "make this a default flavor to use when creating new instances", null = False, db_index = False, blank = True )
  

  # Relations
  
  deployments = ManyToManyField(Deployment, db_index = False, related_name = 'flavors', null = False, through = 'DashboardView_deployments', blank = True )

  class Meta:
      app_label = "core"
      ordering = ('order', 'name')
  
  def __init__(self, *args, **kwargs):
      super(Flavor, self).__init__(*args, **kwargs)
      self.no_sync=True
  
  def __unicode__(self):  return u'%s' % (self.name)
  pass

