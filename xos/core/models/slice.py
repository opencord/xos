

from header import *



from core.models.site import Site 



from core.models.service import Service 



from core.models.serviceclass import ServiceClass 



from core.models.user import User 



from core.models.flavor import Flavor 



from core.models.image import Image 



from core.models.node import Node 






class Slice(XOSBase):
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

  NETWORK_CHOICES = ((None, 'Default'), ('host', 'Host'), ('bridged', 'Bridged'), ('noauto', 'No Automatic Networks'))
  
  def __unicode__(self):  return u'%s' % (self.name)
  
  @property
  def slicename(self):
      return "%s_%s" % (self.site.login_base, self.name)
  
  def save(self, *args, **kwds):
      site = Site.objects.get(id=self.site.id)
      # allow preexisting slices to keep their original name for now
      if not self.id and not self.name.startswith(site.login_base):
          raise XOSValidationError('slice name must begin with %s' % site.login_base)
  
      if self.name == site.login_base+"_":
          raise XOSValidationError('slice name is too short')
  
      if " " in self.name:
          raise XOSValidationError('slice name must not contain spaces')
  
      # set creator on first save
      if not self.creator and hasattr(self, 'caller'):
          self.creator = self.caller
  
      # only admins change a slice's creator
      if 'creator' in self.changed_fields and \
          (not hasattr(self, 'caller') or not self.caller.is_admin):
  
          if (self._initial["creator"]==None) and (self.creator==getattr(self,"caller",None)):
              # it's okay if the creator is being set by the caller to
              # himeself on a new slice object.
              pass
          else:
              raise PermissionDenied("Insufficient privileges to change slice creator")
      
      if not self.creator:
          raise XOSValidationError('slice has no creator')
  
      if self.network=="Private Only":
          # "Private Only" was the default from the old Tenant View
          self.network=None
      self.enforce_choices(self.network, self.NETWORK_CHOICES)
  
      super(Slice, self).save(*args, **kwds)
  
  def can_update(self, user):
      return user.can_update_slice(self)
  
  
  @staticmethod
  def select_by_user(user):
      if user.is_admin:
          qs = Slice.objects.all()
      else:
          from core.models.sliceprivilege import SlicePrivilege 
          from core.models.siteprivilege import SitePrivilege
          # users can see slices they belong to 
          slice_ids = [sp.slice.id for sp in SlicePrivilege.objects.filter(user=user)]
          # pis and admins can see slices at their sites
          sites = [sp.site for sp in SitePrivilege.objects.filter(user=user)\
                      if (sp.role.role == 'pi') or (sp.role.role == 'admin')]
          slice_ids.extend([s.id for s in Slice.objects.filter(site__in=sites)])
          qs = Slice.objects.filter(id__in=slice_ids)
      return qs
  
  """
  def delete(self, *args, **kwds):
      # delete networks associated with this slice
      from core.models.network import Network
      nets = Network.objects.filter(slices=self)
      nets.delete() 
      # delete slice controllers
      slice_controllers = ControllerSlice.objects.filter(slice=self)
      slice_controllers.delete()
      # delete slice privilege
      slice_privileges = SlicePrivilege.objects.filter(slice=self)
      slice_privileges.delete() 
      # continue with normal delete
      super(Slice, self).delete(*args, **kwds) 
  """
  
  pass

