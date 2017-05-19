

from header import *

from core.models.networkparameter import NetworkParameter
from core.models.networkparametertype import NetworkParameterType

class ParameterMixin(object):
    # helper classes for dealing with NetworkParameter

    def get_parameters(self):
        parameter_dict = {}

        instance_type = self.get_content_type_key()
        for param in NetworkParameter.objects.filter(content_type=instance_type, object_id=self.id):
            parameter_dict[param.parameter.name] = param.value

        return parameter_dict

    def set_parameter(self, name, value):
        instance_type = self.get_content_type_key()
        existing_params = NetworkParameter.objects.filter(parameter__name=name, content_type=instance_type, object_id=self.id)
        if existing_params:
            p=existing_params[0]
            p.value = value
            p.save()
        else:
            pt = NetworkParameterType.objects.get(name=name)
            p = NetworkParameter(parameter=pt, content_type=instance_type, object_id=self.id, value=value)
            p.save()

    def unset_parameter(self, name):
        instance_type = self.get_content_type_key()
        existing_params = NetworkParameter.objects.filter(parameter__name=name, content_type=instance_type, object_id=self.id)
        for p in existing_params:
            p.delete()

 


from core.models.network import Network 



from core.models.instance import Instance 








class Port(XOSBase,ParameterMixin):
  # Primitive Fields (Not Relations)
  ip = GenericIPAddressField( help_text = "Instance ip address", max_length = 39, null = True, db_index = False, blank = True )
  port_id = CharField( help_text = "Neutron port id", max_length = 256, null = True, db_index = False, blank = True )
  mac = CharField( help_text = "MAC address associated with this port", max_length = 256, null = True, db_index = False, blank = True )
  xos_created = BooleanField( default = False, null = False, blank = True, db_index = False )
  

  # Relations
  
  network = ForeignKey(Network, db_index = True, related_name = 'links', null = False, blank = False )
  instance = ForeignKey(Instance, db_index = True, related_name = 'ports', null = True, blank = True )

  class Meta:
      unique_together = ('network', 'instance')
  
  def save(self, *args, **kwds):
      if self.instance:
          slice = self.instance.slice
          if (slice not in self.network.permitted_slices.all()) and (slice != self.network.owner) and (not self.network.permit_all_slices):
              # to add a instance to the network, then one of the following must be true:
              #   1) instance's slice is in network's permittedSlices list,
              #   2) instance's slice is network's owner, or
              #   3) network's permitAllSlices is true
              raise ValueError("Slice %s is not allowed to connect to network %s" % (str(slice), str(self.network)))
  
      super(Port, self).save(*args, **kwds)
  
  def __unicode__(self):
      if self.instance:
          return u'%s-%s' % (self.network.name, self.instance.instance_name)
      else:
          return u'%s-unboundport-%s' % (self.network.name, self.id)
  
  def can_update(self, user):
      if self.instance:
          return user.can_update_slice(self.instance.slice)
      if self.network:
          return user.can_update_slice(self.network.owner)
      return False
  
  @staticmethod
  def select_by_user(user):
      if user.is_admin:
          qs = Port.objects.all()
      else:
          instances = Instance.select_by_user(user)
          instance_ids = [instance.id for instance in instances]
          networks = Network.select_by_user(user)
          network_ids = [network.id for network in networks]
          qs = Port.objects.filter(Q(instance__in=instance_ids) | Q(network__in=network_ids))
      return qs
  
  def get_parameters(self):
      # returns parameters from the network, updated by self.
      p={}
      if self.network:
          p = self.network.get_parameters()
      p.update(ParameterMixin.get_parameters(self))
      return p
  
  pass

