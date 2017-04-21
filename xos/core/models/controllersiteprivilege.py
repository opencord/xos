
from header import *





from core.models.controller import Controller 



from core.models.siteprivilege import SitePrivilege 






class ControllerSitePrivilege(PlCoreBase):
  # Primitive Fields (Not Relations)
  role_id = StrippedCharField( help_text = "Keystone id", max_length = 200, null = True, db_index = True, blank = True )
  

  # Relations
  
  controller = ForeignKey(Controller, db_index = True, related_name = 'controllersiteprivileges', null = False, blank = False )
  site_privilege = ForeignKey(SitePrivilege, db_index = True, related_name = 'controllersiteprivileges', null = False, blank = False )

  class Meta:
      unique_together = ('controller', 'site_privilege', 'role_id')
  
  def __unicode__(self):  return u'%s %s' % (self.controller, self.site_privilege)
  
  def can_update(self, user):
      if user.is_readonly:
          return False
      if user.is_admin:
          return True
      cprivs = ControllerSitePrivilege.objects.filter(site_privilege__user=user)
      for cpriv in dprivs:
          if cpriv.site_privilege.role.role == ['admin', 'Admin']:
              return True
      return False
  
  @staticmethod
  def select_by_user(user):
      if user.is_admin:
          qs = ControllerSitePrivilege.objects.all()
      else:
          cpriv_ids = [cp.id for cp in ControllerSitePrivilege.objects.filter(site_privilege__user=user)]
          qs = ControllerSitePrivilege.objects.filter(id__in=cpriv_ids)
      return qs
  pass

