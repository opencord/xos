
from header import *


from service_header import *
 


from core.models.loadablemodule import LoadableModule 






class LoadableModuleResource(PlCoreBase):
  # Primitive Fields (Not Relations)
  name = StrippedCharField( help_text = "Object Name", max_length = 30, null = False, db_index = False, blank = False )
  subdirectory = StrippedCharField( help_text = "optional subdirectory", max_length = 1024, null = True, db_index = False, blank = True )
  kind = StrippedCharField( blank = False, max_length = 30, null = False, db_index = False, choices = (('models', 'Models'), ('admin', 'Admin'), ('admin_template', 'Admin Template'), ('django_library', 'Django Library'), ('synchronizer', 'Synchronizer'), ('rest_service', 'REST API (service)'), ('rest_tenant', 'REST API (tenant)'), ('tosca_custom_types', 'Tosca Custom Types'), ('tosca_resource', 'Tosca Resource'), ('private_key', 'Private Key'), ('public_key', 'Public Key'), ('vendor_js', 'Vendor Javascript')) )
  format = StrippedCharField( blank = False, max_length = 30, null = False, db_index = False, choices = (('python', 'Python'), ('manifest', 'Manifest'), ('docker', 'Docker Container'), ('yaml', 'YAML'), ('raw', 'raw'), ('javascript', 'Javascript')) )
  url = StrippedCharField( help_text = "URL of resource", max_length = 1024, null = True, db_index = False, blank = True )
  

  # Relations
  
  loadable_module = ForeignKey(LoadableModule, help_text = "The Loadable Module this resource is associated with", related_name = 'loadable_module_resources', null = False, db_index = True, blank = False )

  def __unicode__(self): return u'%s' % (self.name)
  
  @property
  def full_url(self):
      if self.loadable_module and self.loadable_module.base_url:
          return urlparse.urljoin(self.loadable_module.base_url, self.url)
      else:
          return self.url
  pass

