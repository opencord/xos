
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

  
  pass

