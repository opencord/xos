

from header import *



from core.models.service import Service 






class Tag(XOSBase):
  # Primitive Fields (Not Relations)
  name = CharField( help_text = "The name of this tag", max_length = 128, null = False, db_index = True, blank = False )
  value = StrippedCharField( help_text = "The value of this tag", max_length = 1024, null = False, db_index = False, blank = False )
  content_type = StrippedCharField( help_text = "Content type id linked to this tag", max_length = 1024, null = False, db_index = False, blank = False )
  object_id = IntegerField( help_text = "Object linked to this tag", null = False, blank = False, db_index = False )
  

  # Relations
  
  service = ForeignKey(Service, help_text = "The Service this Tag is associated with", related_name = 'tags', null = False, db_index = True, blank = False )

  def __unicode__(self):
      return self.name
  
  def can_update(self, user):
      return user.can_update_root()
  
  @classmethod
  def select_by_content_object(cls, obj):
      return cls.objects.filter(content_type=obj.get_content_type_key(), object_id=obj.id)
  
  @staticmethod
  def select_by_user(user):
      return Tag.objects.all()
  pass

