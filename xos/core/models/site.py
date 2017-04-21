
from header import *





from core.models.deployment import Deployment 



from core.models.tag import Tag 






class Site(PlCoreBase):
  # Primitive Fields (Not Relations)
  name = StrippedCharField( help_text = "Name for this Site", max_length = 200, null = False, db_index = False, blank = False )
  site_url = URLField( help_text = "Site's Home URL Page", max_length = 512, null = True, db_index = False, blank = True )
  enabled = BooleanField( default = True, help_text = "Status for this Site", null = False, db_index = False, blank = True )
  hosts_nodes = BooleanField( default = True, help_text = "Indicates whether or not the site host nodes", null = False, db_index = False, blank = True )
  hosts_users = BooleanField( default = True, help_text = "Indicates whether or not the site manages user accounts", null = False, db_index = False, blank = True )
  longitude = FloatField( blank = True, null = True, db_index = False )
  latitude = FloatField( blank = True, null = True, db_index = False )
  login_base = StrippedCharField( help_text = "Prefix for Slices associated with this Site", max_length = 50, null = False, db_index = False, blank = False )
  is_public = BooleanField( default = True, help_text = "Indicates the visibility of this site to other members", null = False, db_index = False, blank = True )
  abbreviated_name = StrippedCharField( db_index = False, max_length = 80, null = False, blank = False )
  

  # Relations
  
  deployments = ManyToManyField(Deployment, help_text = "Select which sites are allowed to host nodes in this deployment", related_name = 'sites', null = False, db_index = False, blank = True )
  tags = GenericRelation(Tag, db_index = False, null = False, blank = True )

  objects = ControllerManager()
  deleted_objects = ControllerDeletionManager()
  
  def __unicode__(self):  return u'%s' % (self.name)
  
  def can_update(self, user):
      return user.can_update_site(self, allow=['pi'])
  
  pass

