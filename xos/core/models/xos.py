
from header import *








class XOS(PlCoreBase):
  # Primitive Fields (Not Relations)
  name = StrippedCharField( default = "XOS", max_length = 200, blank = False, help_text = "Name of XOS", null = False, db_index = False )
  ui_port = IntegerField( default = 80, help_text = "Port for XOS UI", null = False, db_index = False, blank = False )
  bootstrap_ui_port = IntegerField( default = 81, help_text = "Port for XOS Bootstrap UI", null = False, db_index = False, blank = False )
  db_container_name = StrippedCharField( default = "xos_db", max_length = 200, blank = False, help_text = "name of XOS db container", null = False, db_index = False )
  redis_container_name = StrippedCharField( default = "", max_length = 200, blank = True, help_text = "name of XOS redis container", null = False, db_index = False )
  docker_project_name = StrippedCharField( help_text = "docker project name", max_length = 200, null = False, db_index = False, blank = False )
  enable_build = BooleanField( default = True, help_text = "True if Onboarding Synchronizer should build XOS as necessary", null = False, db_index = False, blank = True )
  frontend_only = BooleanField( default = False, help_text = "If True, XOS will not start synchronizer containers", null = False, db_index = False, blank = True )
  source_ui_image = StrippedCharField( default = "xosproject/xos", max_length = 200, null = False, db_index = False, blank = False )
  extra_hosts = StrippedCharField( help_text = "list of hostname mappings that will be passed to docker-compose", max_length = 1024, null = True, db_index = False, blank = True )
  no_start = BooleanField( default = False, help_text = "Do not start the XOS UI inside of the UI docker container", null = False, db_index = False, blank = True )
  

  # Relations
  

  def __unicode__(self):  return u'%s' % (self.name)
  
  def __init__(self, *args, **kwargs):
      super(XOS, self).__init__(*args, **kwargs)
  
  def save(self, *args, **kwds):
      super(XOS, self).save(*args, **kwds)
  
  #    def can_update(self, user):
  #        return user.can_update_site(self.site, allow=['tech'])
  
  def rebuild(self, services=[]):
      # If `services` is empty, then only rebuild the UI
      # Otherwise, only rebuild the services listed in `services`
      with transaction.atomic():
          for loadable_module in self.loadable_modules.all():
              if (services) and (loadable_module.name not in services):
                  continue
              for lmr in loadable_module.loadable_module_resources.all():
                 lmr.save()
              loadable_module.save()
          self.save()
  pass

