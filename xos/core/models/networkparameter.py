
from header import *





from core.models.networkparametertype import NetworkParameterType 



from core.models.contenttype import ContentType 






class NetworkParameter(PlCoreBase):
  # Primitive Fields (Not Relations)
  value = CharField( help_text = "The value of this parameter", max_length = 1024, null = False, db_index = False, blank = False )
  object_id = IntegerField( blank = False, null = False, db_index = False )
  

  # Relations
  
  parameter = ForeignKey(NetworkParameterType, help_text = "The type of the parameter", related_name = 'networkparameters', null = False, db_index = True, blank = False )
  content_type = ForeignKey(ContentType, db_index = True, related_name = 'networkparameter', null = False, blank = False )

  content_object = GenericForeignKey('content_type', 'object_id')
  
  def __unicode__(self):
      return self.parameter.name
  
  pass

