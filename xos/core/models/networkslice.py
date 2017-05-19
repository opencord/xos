

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

 


from core.models.network import Network 



from core.models.slice import Slice 






class NetworkSlice(XOSBase):
  # Primitive Fields (Not Relations)
  

  # Relations
  
  network = ForeignKey(Network, db_index = True, related_name = 'networkslices', null = False, blank = False )
  slice = ForeignKey(Slice, db_index = True, related_name = 'networkslices', null = False, blank = False )

  class Meta:
      unique_together = ('network', 'slice')
  
  def save(self, *args, **kwds):
      slice = self.slice
      if (slice not in self.network.permitted_slices.all()) and (slice != self.network.owner) and (not self.network.permit_all_slices):
          # to add a instance to the network, then one of the following must be true:
          #   1) instance's slice is in network's permittedSlices list,
          #   2) instance's slice is network's owner, or
          #   3) network's permitAllSlices is true
          raise ValueError("Slice %s is not allowed to connect to network %s" % (str(slice), str(self.network)))
  
      super(NetworkSlice, self).save(*args, **kwds)
  
  def __unicode__(self):  return u'%s-%s' % (self.network.name, self.slice.name)
  
  def can_update(self, user):
      return user.can_update_slice(self.slice)
  
  @staticmethod
  def select_by_user(user):
      if user.is_admin:
          qs = NetworkSlice.objects.all()
      else:
          slice_ids = [s.id for s in Slice.select_by_user(user)]
          network_ids = [network.id for network in Network.select_by_user(user)]
          qs = NetworkSlice.objects.filter(Q(slice__in=slice_ids) | Q(network__in=network_ids))
      return qs
  
  pass

