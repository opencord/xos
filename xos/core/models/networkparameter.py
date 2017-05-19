

from header import *



from core.models.networkparametertype import NetworkParameterType 






class NetworkParameter(XOSBase):
  # Primitive Fields (Not Relations)
  value = CharField( help_text = "The value of this parameter", max_length = 1024, null = False, db_index = False, blank = False )
  content_type = StrippedCharField( help_text = "Content type id linked to this network parameter", max_length = 1024, null = False, db_index = False, blank = False )
  object_id = IntegerField( help_text = "Object linked to this NetworkParameter", null = False, blank = False, db_index = False )
  

  # Relations
  
  parameter = ForeignKey(NetworkParameterType, help_text = "The type of the parameter", related_name = 'networkparameters', null = False, db_index = True, blank = False )

  def __unicode__(self):
      return self.parameter.name
  
  pass

