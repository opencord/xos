
from header import *








class Diag(PlCoreBase):
  # Primitive Fields (Not Relations)
  name = StrippedCharField( help_text = "Name of the synchronizer", max_length = 200, null = False, db_index = False, blank = False )
  

  # Relations
  

  @property
  def enacted(self):
      return None
  
  @enacted.setter
  def enacted(self, value):
      pass # Ignore sets, Diag objects are always pending.
  pass

