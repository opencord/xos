
from header import *





from core.models.site import Site 






class SiteCredential(PlCoreBase):
  # Primitive Fields (Not Relations)
  name = CharField( help_text = "The credential type, e.g. ec2", max_length = 128, null = False, db_index = True, blank = False )
  key_id = StrippedCharField( help_text = "The backend id of this credential", max_length = 1024, null = False, db_index = False, blank = False )
  enc_value = CharField( help_text = "The key value of this credential", max_length = 1024, null = False, db_index = False, blank = False )
  

  # Relations
  
  site = ForeignKey(Site, help_text = "The User this credential is associated with", related_name = 'sitecredentials', null = False, db_index = True, blank = False )

  def __unicode__(self):
      return self.name
  
  
  pass

