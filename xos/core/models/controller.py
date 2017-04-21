
from header import *





from core.models.deployment import Deployment 






class Controller(PlCoreBase):
  # Primitive Fields (Not Relations)
  name = StrippedCharField( help_text = "Name of the Controller", max_length = 200, null = False, db_index = False, blank = False )
  backend_type = StrippedCharField( help_text = "Type of compute controller, e.g. EC2, OpenStack, or OpenStack version", max_length = 200, null = False, db_index = False, blank = False )
  version = StrippedCharField( help_text = "Controller version", max_length = 200, null = False, db_index = False, blank = False )
  auth_url = StrippedCharField( help_text = "Auth url for the compute controller", max_length = 200, null = True, db_index = False, blank = True )
  admin_user = StrippedCharField( help_text = "Username of an admin user at this controller", max_length = 200, null = True, db_index = False, blank = True )
  admin_password = StrippedCharField( help_text = "Password of theadmin user at this controller", max_length = 200, null = True, db_index = False, blank = True )
  admin_tenant = StrippedCharField( help_text = "Name of the tenant the admin user belongs to", max_length = 200, null = True, db_index = False, blank = True )
  domain = StrippedCharField( help_text = "Name of the domain this controller belongs to", max_length = 200, null = True, db_index = False, blank = True )
  rabbit_host = StrippedCharField( help_text = "IP address of rabbitmq server at this controller", max_length = 200, null = True, db_index = False, blank = True )
  rabbit_user = StrippedCharField( help_text = "Username of rabbitmq server at this controller", max_length = 200, null = True, db_index = False, blank = True )
  rabbit_password = StrippedCharField( help_text = "Password of rabbitmq server at this controller", max_length = 200, null = True, db_index = False, blank = True )
  

  # Relations
  
  deployment = ForeignKey(Deployment, db_index = True, related_name = 'controllerdeployments', null = False, blank = False )

  objects = ControllerManager()
  deleted_objects = ControllerDeletionManager()
  
  def __init__(self, *args, **kwargs):
      super(Controller, self).__init__(*args, **kwargs)
      self.no_sync=True
  
  def __unicode__(self):  return u'%s %s %s' % (self.name, self.backend_type, self.version)
  
  @property
  def auth_url_v3(self):
      if self.auth_url and self.auth_url[-1] == '/':
          return '{}/v3/'.format('/'.join(self.auth_url.split('/')[:-2]))
      else:
          return '{}/v3/'.format('/'.join(self.auth_url.split('/')[:-1]))
  
  @staticmethod
  def select_by_user(user):
  
      if user.is_admin:
          qs = Controller.objects.all()
      else:
          from core.models.deploymentprivilege import DeploymentPrivilege
          deployments = [dp.deployment for dp in DeploymentPrivilege.objects.filter(user=user, role__role__in=['Admin', 'admin'])]
          qs = Controller.objects.filter(deployment__in=deployments)
      return qs
  pass

