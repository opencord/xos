
from header import *





from core.models.loadablemodule import LoadableModule




class XOSComponent(LoadableModule):
  # Primitive Fields (Not Relations)
  image = StrippedCharField( help_text = "docker image name", max_length = 200, null = False, db_index = False, blank = False )
  command = StrippedCharField( help_text = "docker run command", max_length = 1024, null = True, db_index = False, blank = True )
  ports = StrippedCharField( help_text = "port binding", max_length = 200, null = True, db_index = False, blank = True )
  extra = StrippedCharField( help_text = "extra information needed by containers", max_length = 200, null = True, db_index = False, blank = True )
  no_start = BooleanField( default = False, help_text = "Do not start the Component", null = False, db_index = False, blank = True )
  

  # Relations
  

  
  pass

