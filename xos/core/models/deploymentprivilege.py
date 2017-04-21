
from header import *





from core.models.user import User 



from core.models.deployment import Deployment 



from core.models.deploymentrole import DeploymentRole 






class DeploymentPrivilege(PlCoreBase):
  # Primitive Fields (Not Relations)
  

  # Relations
  
  user = ForeignKey(User, db_index = True, related_name = 'deploymentprivileges', null = False, blank = False )
  deployment = ForeignKey(Deployment, db_index = True, related_name = 'deploymentprivileges', null = False, blank = False )
  role = ForeignKey(DeploymentRole, db_index = True, related_name = 'deploymentprivileges', null = False, blank = False )

  # Relations

  class Meta:
      unique_together = ('user', 'deployment', 'role')
  
  def __unicode__(self):  return u'%s %s %s' % (self.deployment, self.user, self.role)
  
  def can_update(self, user):
      return user.can_update_deployment(self)
  
  @staticmethod
  def select_by_user(user):
      from core.models.deploymentprivilege import DeploymentPrivilege
      if user.is_admin:
          qs = DeploymentPrivilege.objects.all()
      else:
          dpriv_ids = [dp.id for dp in DeploymentPrivilege.objects.filter(user=user)]
          qs = DeploymentPrivilege.objects.filter(id__in=dpriv_ids)
      return qs
  pass
  
  pass

