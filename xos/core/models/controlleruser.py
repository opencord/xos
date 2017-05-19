

from header import *



from core.models.user import User 



from core.models.controller import Controller 






class ControllerUser(XOSBase):
  # Primitive Fields (Not Relations)
  kuser_id = StrippedCharField( help_text = "Keystone user id", max_length = 200, null = True, db_index = False, blank = True )
  

  # Relations
  
  user = ForeignKey(User, db_index = True, related_name = 'controllerusers', null = False, blank = False )
  controller = ForeignKey(Controller, db_index = True, related_name = 'controllersusers', null = False, blank = False )

  objects = ControllerLinkManager()
  deleted_objects = ControllerLinkDeletionManager()
  
  class Meta:
      unique_together = ('user', 'controller')
  
  def __unicode__(self):  return u'%s %s' % (self.controller, self.user)
  
  @staticmethod
  def select_by_user(user):
      if user.is_admin:
          qs = ControllerUser.objects.all()
      else:
          users = User.select_by_user(user)
          qs = ControllerUser.objects.filter(user__in=users)
      return qs
  
  def can_update(self, user):
      return user.can_update_root()    
  
  pass

