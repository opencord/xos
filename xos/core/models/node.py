
from header import *





from core.models.sitedeployment import SiteDeployment 



from core.models.site import Site 



from core.models.tag import Tag 






class Node(PlCoreBase):
  # Primitive Fields (Not Relations)
  name = StrippedCharField( help_text = "Name of the Node", max_length = 200, null = False, db_index = False, blank = False )
  

  # Relations
  
  site_deployment = ForeignKey(SiteDeployment, db_index = True, related_name = 'nodes', null = False, blank = False )
  site = ForeignKey(Site, db_index = True, related_name = 'nodes', null = True, blank = True )
  tags = GenericRelation(Tag, db_index = False, null = False, blank = True )

  def __unicode__(self):  return u'%s' % (self.name)
  
  def __init__(self, *args, **kwargs):
      super(Node, self).__init__(*args, **kwargs)
      self.no_sync=True
  
  def can_update(self, user):
      return user.can_update_site(self.site, allow=['tech'])
  
  def save(self, *args, **kwds):
      if self.site is None and self.site_deployment is not None:
          self.site = self.site_deployment.site
  
      super(Node, self).save(*args, **kwds)
  pass

