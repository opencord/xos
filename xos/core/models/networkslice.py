
from header import *

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






class NetworkSlice(PlCoreBase):
  # Primitive Fields (Not Relations)
  

  # Relations
  
  network = ForeignKey(Network, db_index = True, related_name = 'networkslices', null = False, blank = False )
  slice = ForeignKey(Slice, db_index = True, related_name = 'networkslices', null = False, blank = False )

  class Meta:
      unique_together = ('network', 'controller')
  
  def tologdict(self):
      from core.models.controllernetwork import ControllerNetwork
      d=super(ControllerNetwork,self).tologdict()
      try:
          d['network_name']=self.network.name
          d['controller_name']=self.controller.name
      except:
          pass
      return d
  
  @staticmethod
  def select_by_user(user):
      from core.models.controllernetwork import ControllerNetwork
      if user.is_admin:
          qs = ControllerNetwork.objects.all()
      else:
          slices = Slice.select_by_user(user)
          networks = Network.objects.filter(owner__in=slices)
          qs = ControllerNetwork.objects.filter(network__in=networks)
      return qs
  
  pass

