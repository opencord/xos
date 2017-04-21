
from header import *





from core.models.xoscomponent import XOSComponent 






class XOSComponentLink(PlCoreBase):
  # Primitive Fields (Not Relations)
  container = StrippedCharField( help_text = "container to link", max_length = 200, null = False, db_index = False, blank = False )
  alias = StrippedCharField( help_text = "alias for the link", max_length = 200, null = False, db_index = False, blank = False )
  kind = CharField( default = "internal", choices = (('internal', 'Internal'), ('external', 'External')), max_length = 20, blank = False, null = False, db_index = False )
  

  # Relations
  
  component = ForeignKey(XOSComponent, help_text = "The Component object for this Link", related_name = 'links', null = False, db_index = True, blank = False )

  def save(self, *args, **kwds):
      # If this is a new object, then check to make sure it doesn't already exist
      if not self.pk:
          existing = XOSComponentLink.objects.filter(container=self.container, alias=self.alias)
          if len(existing) > 0:
              raise XOSValidationError('XOSComponentLink for %s:%s already defined' % (self.container, self.alias))
      super(XOSComponentLink, self).save(*args, **kwds)
  pass

