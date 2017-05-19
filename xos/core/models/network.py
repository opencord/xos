

from network_header import *

from core.models.networkparameter import NetworkParameter

class ParameterMixin(object):
    # helper classes for dealing with NetworkParameter

    def get_parameters(self):
        parameter_dict = {}

        instance_type = ContentType.objects.get_for_model(self)
        for param in NetworkParameter.objects.filter(content_type__pk=instance_type.id, object_id=self.id):
            parameter_dict[param.parameter.name] = param.value

        return parameter_dict

    def set_parameter(self, name, value):
        instance_type = ContentType.objects.get_for_model(self)
        existing_params = NetworkParameter.objects.filter(parameter__name=name, content_type__pk=instance_type.id, object_id=self.id)
        if existing_params:
            p=existing_params[0]
            p.value = value
            p.save()
        else:
            from core.models.networkparametertype import NetworkParameterType
            pt = NetworkParameterType.objects.get(name=name)
            p = NetworkParameter(parameter=pt, content_type=instance_type, object_id=self.id, value=value)
            p.save()

    def unset_parameter(self, name):
        instance_type = ContentType.objects.get_for_model(self)
        existing_params = NetworkParameter.objects.filter(parameter__name=name, content_type__pk=instance_type.id, object_id=self.id)
        for p in existing_params:
            p.delete()

 


from core.models.networktemplate import NetworkTemplate 



from core.models.slice import Slice 



from core.models.slice import Slice 



from core.models.slice import Slice 



from core.models.instance import Instance 








class Network(XOSBase,ParameterMixin):
  # Primitive Fields (Not Relations)
  name = CharField( blank = False, max_length = 32, null = False, db_index = False )
  subnet = CharField( blank = True, max_length = 32, null = False, db_index = False )
  start_ip = CharField( blank = True, max_length = 32, null = False, db_index = False )
  end_ip = CharField( blank = True, max_length = 32, null = False, db_index = False )
  ports = CharField( blank = True, max_length = 1024, null = True, db_index = False )
  labels = CharField( blank = True, max_length = 1024, null = True, db_index = False )
  guaranteed_bandwidth = IntegerField( default = 0, null = False, blank = False, db_index = False )
  permit_all_slices = BooleanField( default = False, null = False, blank = True, db_index = False )
  topology_parameters = TextField( blank = True, null = True, db_index = False )
  controller_url = CharField( blank = True, max_length = 1024, null = True, db_index = False )
  controller_parameters = TextField( blank = True, null = True, db_index = False )
  network_id = CharField( help_text = "Quantum network", max_length = 256, null = True, db_index = False, blank = True )
  router_id = CharField( help_text = "Quantum router id", max_length = 256, null = True, db_index = False, blank = True )
  subnet_id = CharField( help_text = "Quantum subnet id", max_length = 256, null = True, db_index = False, blank = True )
  autoconnect = BooleanField( default = True, help_text = "This network can be autoconnected to the slice that owns it", null = False, db_index = False, blank = True )
  

  # Relations
  
  template = ForeignKey(NetworkTemplate, db_index = True, related_name = 'network', null = False, blank = False )
  owner = ForeignKey(Slice, help_text = "Slice that owns control of this Network", related_name = 'ownedNetworks', null = False, db_index = True, blank = False )
  permitted_slices = ManyToManyField(Slice, db_index = False, related_name = 'availableNetworks', null = False, blank = True )
  slices = ManyToManyField(Slice, db_index = False, related_name = 'networks', null = False, through = 'NetworkSlice', blank = True )
  instances = ManyToManyField(Instance, db_index = False, related_name = 'networks', null = False, through = 'Port', blank = True )

  def __unicode__(self):  return u'%s' % (self.name)
  
  def save(self, *args, **kwds):
      if (not self.subnet) and (NO_OBSERVER):
          from util.network_subnet_allocator import find_unused_subnet
          self.subnet = find_unused_subnet(existing_subnets=[x.subnet for x in Network.objects.all()])
          print "DEF_MOD_NET_IP", self.start_ip
      super(Network, self).save(*args, **kwds)
  
  def can_update(self, user):
      return user.can_update_slice(self.owner)
  
  @property
  def nat_list(self):
      return ParseNatList(self.ports)
  
  @staticmethod
  def select_by_user(user):
      if user.is_admin:
          qs = Network.objects.all()
      else:
          slices = Slice.select_by_user(user)
          #slice_ids = [s.id for s in Slice.select_by_user(user)]
          qs = Network.objects.filter(owner__in=slices)
      return qs
  
  def get_parameters(self):
      # returns parameters from the template, updated by self.
      p={}
      if self.template:
          p = self.template.get_parameters()
      p.update(ParameterMixin.get_parameters(self))
      return p
  
  pass

