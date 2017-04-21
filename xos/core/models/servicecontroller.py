
from header import *

from service_header import *



from core.models.loadablemodule import LoadableModule




class ServiceController(LoadableModule):
  # Primitive Fields (Not Relations)
  synchronizer_run = StrippedCharField( help_text = "synchronizer run command", max_length = 1024, null = True, db_index = False, blank = True )
  synchronizer_config = StrippedCharField( help_text = "synchronizer config file", max_length = 1024, null = True, db_index = False, blank = True )
  image = StrippedCharField( help_text = "docker image name", max_length = 200, null = True, db_index = False, blank = True )
  no_start = BooleanField( default = False, help_text = "Do not start the Synchronizer", null = False, db_index = False, blank = True )
  no_build = BooleanField( default = False, help_text = "Do not build the Synchronizer container", null = False, db_index = False, blank = True )
  no_deploy = BooleanField( default = False, help_text = "Do not add synchronizer container to onboarding-docker-compose", null = False, db_index = False, blank = True )
  

  # Relations
  

  
  pass

