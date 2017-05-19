

from header import *



from core.models.slice import Slice 






class SliceTag(XOSBase):
  # Primitive Fields (Not Relations)
  name = StrippedCharField( choices = (('privatekey', 'Private Key'), ('publickey', 'Public Key')), max_length = 30, blank = False, help_text = "The name of this tag", null = False, db_index = False )
  value = StrippedCharField( help_text = "The value of this tag", max_length = 1024, null = False, db_index = False, blank = False )
  

  # Relations
  
  slice = ForeignKey(Slice, db_index = True, related_name = 'slicetags', null = False, blank = False )

  def can_update(self, user):
      return user.can_update_slice(self.slice)
  
  @staticmethod
  def select_by_user(user):
      if user.is_admin:
          qs = SliceTag.objects.all()
      else:
          slices = Slice.select_by_user(user)
          qs = SliceTag.objects.filter(slice__in=slices)
      return qs
  pass

