
from header import *


from service_header import *
 


from core.models.xos import XOS 






class LoadableModule(PlCoreBase):
  # Primitive Fields (Not Relations)
  name = StrippedCharField( help_text = "Service Name", max_length = 30, null = False, db_index = False, blank = False )
  base_url = StrippedCharField( help_text = "Base URL, allows use of relative URLs for resources", max_length = 1024, null = True, db_index = False, blank = True )
  version = StrippedCharField( default = "1.0.0", max_length = 30, blank = True, help_text = "Version of Service Controller", null = True, db_index = False )
  provides = StrippedCharField( help_text = "Comma-separated list of things provided", max_length = 254, null = True, db_index = False, blank = True )
  requires = StrippedCharField( help_text = "Comma-separated list of required Service Controllers", max_length = 254, null = True, db_index = False, blank = True )
  

  # Relations
  
  xos = ForeignKey(XOS, related_name = 'loadable_modules', default = get_xos, blank = False, help_text = "Pointer to XOS", null = False, db_index = True )

  def __unicode__(self): return u'%s' % (self.name)
  
  def save(self, *args, **kwargs):
     super(LoadableModule, self).save(*args, **kwargs)
  
     # This is necessary, as the XOS syncstep handles rerunning the docker-
     # compose.
     # TODO: Update synchronizer and replace with watcher functionality
     if self.xos:
         # force XOS to rebuild
         self.xos.save(update_fields=["updated"])
  
  def get_provides_list(self):
      prov_list = []
      if self.provides and self.provides.strip():
          for prov in self.provides.split(","):
              prov=prov.strip()
              if "=" in prov:
                  (name, version) = prov.split("=",1)
                  name = name.strip()
                  version = version.strip()
              else:
                  name = prov
                  version = "1.0.0"
              prov_list.append( {"name": name, "version": version} )
  
      # every controller provides itself
      prov_list.append( {"name": self.name, "version": self.version} )
  
      return prov_list
  
  
  @classmethod
  def dependency_check(cls, dep_list):
      missing = []
      satisfied = []
      operators = {">=": operator.ge,
                   "<=": operator.le,
                   ">": operator.gt,
                   "<": operator.lt,
                   "!=": operator.ne,
                   "=": operator.eq}
      from core.models.servicecontroller import ServiceController
  
      for dep in dep_list:
          dep = dep.strip()
          name = dep
          version = None
          this_op = None
          for op in operators.keys():
              if op in dep:
                  (name, version) = dep.split(op,1)
                  name = name.strip()
                  version = version.strip()
                  this_op = operators[op]
                  break
          found=False
          scs = ServiceController.objects.all()
          for sc in scs:
              for provide in sc.get_provides_list():
                  if (provide["name"] != name):
                      continue
                  if not this_op:
                      satisfied.append(sc)
                      found=True
                      break
                  elif this_op(LooseVersion(provide["version"]), LooseVersion(version)):
                      satisfied.append(sc)
                      found=True
                      break
          if not found:
              missing.append(dep)
  
      return (satisfied, missing)
  pass

