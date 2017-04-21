
from header import *





from core.models.user import User 






class Program(PlCoreBase):
  # Primitive Fields (Not Relations)
  name = StrippedCharField( help_text = "Service Name", max_length = 30, null = False, db_index = False, blank = False )
  description = CharField( help_text = "Description of Service", max_length = 254, null = True, db_index = False, blank = True )
  kind = StrippedCharField( choices = (('tosca', 'Tosca'),), max_length = 30, blank = False, help_text = "Kind of service", null = False, db_index = False )
  command = StrippedCharField( choices = (('run', 'Run'), ('destroy', 'Destroy')), max_length = 30, blank = True, help_text = "Command to run", null = True, db_index = False )
  contents = TextField( help_text = "Contents of Program", null = True, blank = True, db_index = False )
  output = TextField( help_text = "Output of Program", null = True, blank = True, db_index = False )
  messages = TextField( help_text = "Debug messages", null = True, blank = True, db_index = False )
  status = CharField( help_text = "Status of program", max_length = 30, null = True, db_index = False, blank = True )
  

  # Relations
  
  owner = ForeignKey(User, db_index = True, related_name = 'programs', null = True, blank = False )

  @classmethod
  def select_by_user(cls, user):
      return cls.objects.all()
  
  def __unicode__(self): return u'%s' % (self.name)
  
  def can_update(self, user):
      return True
  
  def save(self, *args, **kwargs):
      # set creator on first save
      if not self.owner and hasattr(self, 'caller'):
          self.owner = self.caller
  
      if (self.command in ["run", "destroy"]) and (self.status in ["complete", "exception"]):
          self.status = "queued"
  
      super(Program, self).save(*args, **kwargs)
  pass

