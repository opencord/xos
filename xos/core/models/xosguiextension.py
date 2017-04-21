
from header import *








class XOSGuiExtension(PlCoreBase):
  # Primitive Fields (Not Relations)
  name = StrippedCharField( help_text = "Name of the GUI Extensions", max_length = 200, null = False, db_index = False, blank = False )
  files = StrippedCharField( help_text = "List of comma separated file composing the view", max_length = 1024, null = False, db_index = False, blank = False )
  

  # Relations
  

  """Persist GUI Extension"""
  class Meta:
      app_label = "core"
  
  pass

