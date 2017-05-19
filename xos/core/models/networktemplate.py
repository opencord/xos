

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

 







class NetworkTemplate(XOSBase,ParameterMixin):
  # Primitive Fields (Not Relations)
  name = CharField( blank = False, max_length = 32, null = False, db_index = False )
  description = CharField( blank = True, max_length = 1024, null = True, db_index = False )
  guaranteed_bandwidth = IntegerField( default = 0, null = False, blank = False, db_index = False )
  visibility = CharField( default = "private", choices = (('public', 'public'), ('private', 'private')), max_length = 30, blank = False, null = False, db_index = False )
  translation = CharField( default = "none", choices = (('none', 'none'), ('NAT', 'NAT')), max_length = 30, blank = False, null = False, db_index = False )
  access = CharField( choices = ((None, 'None'), ('indirect', 'Indirect'), ('direct', 'Direct')), max_length = 30, blank = True, help_text = "Advertise this network as a means for other slices to contact this slice", null = True, db_index = False )
  shared_network_name = CharField( blank = True, max_length = 30, null = True, db_index = False )
  shared_network_id = CharField( help_text = "Quantum network", max_length = 256, null = True, db_index = False, blank = True )
  topology_kind = CharField( default = "bigswitch", choices = (('bigswitch', 'BigSwitch'), ('physical', 'Physical'), ('custom', 'Custom')), max_length = 30, blank = False, null = False, db_index = False )
  controller_kind = CharField( blank = True, max_length = 30, null = True, db_index = False, choices = ((None, 'None'), ('onos', 'ONOS'), ('custom', 'Custom')) )
  vtn_kind = CharField( default = "PRIVATE", choices = (('PRIVATE', 'Private'), ('PUBLIC', 'Public'), ('MANAGEMENT_LOCAL', 'Management Local'), ('MANAGEMENT_HOST', 'Management Host'), ('VSG', 'VSG'), ('ACCESS_AGENT', 'Access Agent')), max_length = 30, blank = True, null = True, db_index = False )
  

  # Relations
  

  ACCESS_CHOICES = ((None, 'None'), ('indirect', 'Indirect'), ('direct', 'Direct'))
  
  def __init__(self, *args, **kwargs):
      super(NetworkTemplate, self).__init__(*args, **kwargs)
  
      if (self.topology_kind=="BigSwitch"):
          print >> sys.stderr, "XXX warning: topology_kind invalid case"
          self.topology_kind="bigswitch"
      elif (self.topology_kind=="Physical"):
          print >> sys.stderr, "XXX warning: topology_kind invalid case"
          self.topology_kind="physical"
      elif (self.topology_kind=="Custom"):
          print >> sys.stderr, "XXX warning: topology_kind invalid case"
          self.toplogy_kind="custom"
  
  def save(self, *args, **kwargs):
      self.enforce_choices(self.access, self.ACCESS_CHOICES)
      super(NetworkTemplate, self).save(*args, **kwargs)
  
  def __unicode__(self):  return u'%s' % (self.name)
  
  pass

