
from header import *





from core.models.site import Site 



from core.models.service import Service 



from core.models.serviceclass import ServiceClass 



from core.models.user import User 



from core.models.flavor import Flavor 



from core.models.image import Image 



from core.models.node import Node 



from core.models.tag import Tag 






class Slice(PlCoreBase):
  # Primitive Fields (Not Relations)
  name = StrippedCharField( help_text = "The Name of the Slice", max_length = 80, null = False, db_index = False, blank = False )
  enabled = BooleanField( default = True, help_text = "Status for this Slice", null = False, db_index = False, blank = True )
  omf_friendly = BooleanField( default = False, null = False, blank = True, db_index = False )
  description = CharField( help_text = "High level description of the slice and expected activities", max_length = 1024, null = False, db_index = False, blank = True )
  slice_url = URLField( db_index = False, max_length = 512, null = False, blank = True )
  max_instances = IntegerField( default = 10, null = False, blank = False, db_index = False )
  network = CharField( blank = True, max_length = 256, null = True, db_index = False, choices = ((None, 'Default'), ('host', 'Host'), ('bridged', 'Bridged'), ('noauto', 'No Automatic Networks')) )
  exposed_ports = CharField( blank = True, max_length = 256, null = True, db_index = False )
  mount_data_sets = StrippedCharField( default = "GenBank", max_length = 256, null = True, db_index = False, blank = True )
  default_isolation = CharField( default = "vm", choices = (('vm', 'Virtual Machine'), ('container', 'Container'), ('container_vm', 'Container In VM')), max_length = 30, blank = False, null = False, db_index = False )
  

  # Relations
  
  site = ForeignKey(Site, help_text = "The Site this Slice belongs to", related_name = 'slices', null = False, db_index = True, blank = False )
  service = ForeignKey(Service, db_index = True, related_name = 'slices', null = True, blank = True )
  serviceClass = ForeignKey(ServiceClass, db_index = True, related_name = 'slices', null = True, blank = True )
  creator = ForeignKey(User, db_index = True, related_name = 'slices', null = True, blank = True )
  default_flavor = ForeignKey(Flavor, db_index = True, related_name = 'slices', null = True, blank = True )
  default_image = ForeignKey(Image, db_index = True, related_name = 'slices', null = True, blank = True )
  default_node = ForeignKey(Node, db_index = True, related_name = 'slices', null = True, blank = True )
  tags = GenericRelation(Tag, db_index = False, null = False, blank = True )

  def __unicode__(self):  return u'%s' % (self.name)
  
  @property
  def slicename(self):
      return "%s_%s" % (self.site.login_base, self.name)
  
  def can_update(self, user):
      return user.can_update_slice(self)
  
  @staticmethod
  def select_by_user(user):
      if user.is_admin:
          qs = Slice.objects.all()
      else:
          from core.models.sliceprivilege import SlicePrivilege 
          # users can see slices they belong to 
          slice_ids = [sp.slice.id for sp in SlicePrivilege.objects.filter(user=user)]
          # pis and admins can see slices at their sites
          sites = [sp.site for sp in SitePrivilege.objects.filter(user=user)\
                      if (sp.role.role == 'pi') or (sp.role.role == 'admin')]
          slice_ids.extend([s.id for s in Slice.objects.filter(site__in=sites)])
          qs = Slice.objects.filter(id__in=slice_ids)
      return qs
  pass

