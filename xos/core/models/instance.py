
from header import *

from instance_header import *



from core.models.image import Image 



from core.models.user import User 



from core.models.slice import Slice 



from core.models.deployment import Deployment 



from core.models.node import Node 



from core.models.flavor import Flavor 





from core.models.tag import Tag 






class Instance(PlCoreBase):
  # Primitive Fields (Not Relations)
  instance_id = StrippedCharField( help_text = "Nova instance id", max_length = 200, null = True, db_index = False, blank = True )
  instance_uuid = StrippedCharField( help_text = "Nova instance uuid", max_length = 200, null = True, db_index = False, blank = True )
  name = StrippedCharField( help_text = "Instance name", max_length = 200, null = False, db_index = False, blank = False )
  instance_name = StrippedCharField( help_text = "OpenStack generated name", max_length = 200, null = True, db_index = False, blank = True )
  ip = GenericIPAddressField( help_text = "Instance ip address", max_length = 39, null = True, db_index = False, blank = True )
  numberCores = IntegerField( default = 0, help_text = "Number of cores for instance", null = False, db_index = False, blank = False )
  userData = TextField( help_text = "user_data passed to instance during creation", null = True, blank = True, db_index = False )
  isolation = CharField( default = "vm", choices = (('vm', 'Virtual Machine'), ('container', 'Container'), ('container_vm', 'Container In VM')), max_length = 30, blank = False, null = False, db_index = False )
  volumes = TextField( help_text = "Comma-separated list of directories to expose to parent context", null = True, blank = True, db_index = False )
  

  # Relations
  
  image = ForeignKey(Image, db_index = True, related_name = 'instances', null = False, blank = False )
  creator = ForeignKey(User, db_index = True, related_name = 'instances', null = True, blank = True )
  slice = ForeignKey(Slice, db_index = True, related_name = 'instances', null = False, blank = False )
  deployment = ForeignKey(Deployment, db_index = True, related_name = 'instance_deployment', null = False, blank = False )
  node = ForeignKey(Node, db_index = True, related_name = 'instances', null = False, blank = False )
  flavor = ForeignKey(Flavor, related_name = 'instance', default = get_default_flavor, blank = False, help_text = "Flavor of this instance", null = False, db_index = True )
  parent = ForeignKey('self', help_text = "Parent Instance for containers nested inside of VMs", related_name = 'instance', null = True, db_index = True, blank = True )
  tags = GenericRelation(Tag, db_index = False, null = False, blank = True )

  objects = InstanceManager()
  deleted_objects = InstanceDeletionManager()
  
  def get_controller (self):
      return self.node.site_deployment.controller
  
  def tologdict(self):
      d=super(Instance,self).tologdict()
      try:
          d['slice_name']=self.slice.name
          d['controller_name']=self.get_controller().name
      except:
          pass
      return d
  
  def __unicode__(self):
      if self.name and Slice.objects.filter(id=self.slice_id) and (self.name != self.slice.name):
          # NOTE: The weird check on self.slice_id was due to a problem when
          #   deleting the slice before the instance.
          return u'%s' % self.name
      elif self.instance_name:
          return u'%s' % (self.instance_name)
      elif self.id:
          return u'uninstantiated-%s' % str(self.id)
      elif self.slice:
          return u'unsaved-instance on %s' % self.slice.name
      else:
          return u'unsaved-instance'
  
  def save(self, *args, **kwds):
      if not self.name:
          self.name = self.slice.name
      if not self.creator and hasattr(self, 'caller'):
          self.creator = self.caller
      if not self.creator:
          raise ValidationError('instance has no creator')
  
      if (self.isolation == "container") or (self.isolation == "container_vm"):
          if (self.image.kind != "container"):
             raise ValidationError("Container instance must use container image")
      elif (self.isolation == "vm"):
          if (self.image.kind != "vm"):
             raise ValidationError("VM instance must use VM image")
  
      if (self.isolation == "container_vm") and (not self.parent):
          raise ValidationError("Container-vm instance must have a parent")
  
      if (self.parent) and (self.isolation != "container_vm"):
          raise ValidationError("Parent field can only be set on Container-vm instances")
  
      if (self.slice.creator != self.creator):
          from core.models.sliceprivilege import SlicePrivilege
          # Check to make sure there's a slice_privilege for the user. If there
          # isn't, then keystone will throw an exception inside the observer.
          slice_privs = SlicePrivilege.objects.filter(slice=self.slice, user=self.creator)
          if not slice_privs:
              raise ValidationError('instance creator has no privileges on slice')
  
  # XXX smbaker - disabled for now, was causing fault in tenant view create slice
  #        if not self.controllerNetwork.test_acl(slice=self.slice):
  #            raise exceptions.ValidationError("Deployment %s's ACL does not allow any of this slice %s's users" % (self.controllerNetwork.name, self.slice.name))
  
      super(Instance, self).save(*args, **kwds)
  
  def can_update(self, user):
      return user.can_update_slice(self.slice)
  
  def all_ips(self):
      ips={}
      for ns in self.ports.all():
         if ns.ip:
             ips[ns.network.name] = ns.ip
      return ips
  
  def all_ips_string(self):
      result = []
      ips = self.all_ips()
      for key in sorted(ips.keys()):
          #result.append("%s = %s" % (key, ips[key]))
          result.append(ips[key])
      return ", ".join(result)
  all_ips_string.short_description = "addresses"
  
  def get_public_ip(self):
      for ns in self.ports.all():
          if (ns.ip) and (ns.network.template.visibility=="public") and (ns.network.template.translation=="none"):
              return ns.ip
      return None
  
  # return an address on nat-net
  def get_network_ip(self, pattern):
      for ns in self.ports.all():
          if pattern in ns.network.name.lower():
              return ns.ip
      return None
  
  # return an address that the synchronizer can use to SSH to the instance
  def get_ssh_ip(self):
      # first look specifically for a management_local network
      for ns in self.ports.all():
          if ns.network.template and ns.network.template.vtn_kind=="MANAGEMENT_LOCAL":
              return ns.ip
  
      # for compatibility, now look for any management network
      management=self.get_network_ip("management")
      if management:
          return management
  
      # if all else fails, look for nat-net (for OpenCloud?)
      return self.get_network_ip("nat")
  
  @staticmethod
  def select_by_user(user):
      if user.is_admin:
          qs = Instance.objects.all()
      else:
          slices = Slice.select_by_user(user)
          qs = Instance.objects.filter(slice__in=slices)
      return qs
  
  def get_cpu_stats(self):
      filter = 'instance_id=%s'%self.instance_id
      return monitor.get_meter('cpu',filter,None)
  
  def get_bw_stats(self):
      filter = 'instance_id=%s'%self.instance_id
      return monitor.get_meter('network.outgoing.bytes',filter,None)
  
  def get_node_stats(self):
      # Note sure what should go back here
      return 1
  
  def get_ssh_command(self):
      if (not self.instance_id) or (not self.node) or (not self.instance_name):
          return None
      else:
          return 'ssh -o "ProxyCommand ssh -q %s@%s" ubuntu@%s' % (self.instance_id, self.node.name, self.instance_name)
  
  def get_public_keys(self):
      from core.models.sliceprivilege import SlicePrivilege
      slice_memberships = SlicePrivilege.objects.filter(slice=self.slice)
      pubkeys = set([sm.user.public_key for sm in slice_memberships if sm.user.public_key])
  
      if self.creator.public_key:
          pubkeys.add(self.creator.public_key)
  
      if self.slice.creator.public_key:
          pubkeys.add(self.slice.creator.public_key)
  
      if self.slice.service and self.slice.service.public_key:
          pubkeys.add(self.slice.service.public_key)
  
      return pubkeys
  pass

def controller_setter(instance, **kwargs):
    try:
        instance.controller = instance.node.site_deployment.controller
    except:
        instance.controller = None

models.signals.post_init.connect(controller_setter, Instance)
