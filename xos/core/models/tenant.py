

from header import *
from service_header import *
 


from core.models.service import Service 



from core.models.service import Service 





from core.models.user import User 



from core.models.tenantroot import TenantRoot 



from core.models.network import Network 








class Tenant(XOSBase,AttributeMixin):
  # Primitive Fields (Not Relations)
  name = StrippedCharField( db_index = False, max_length = 200, null = True, blank = True )
  kind = StrippedCharField( default = "generic", max_length = 30, null = False, db_index = False, blank = False )
  service_specific_id = StrippedCharField( db_index = False, max_length = 30, null = True, blank = True )
  service_specific_attribute = TextField( blank = True, null = True, db_index = False )
  connect_method = CharField( default = "na", choices = (('public', 'Public'), ('private', 'Private'), ('private-unidirectional', 'Private Unidirectional'), ('na', 'Not Applicable')), max_length = 30, blank = False, null = False, db_index = False )
  

  # Relations
  
  provider_service = ForeignKey(Service, db_index = True, related_name = 'provided_tenants', null = False, blank = False )
  subscriber_service = ForeignKey(Service, db_index = True, related_name = 'subscribed_tenants', null = True, blank = True )
  subscriber_tenant = ForeignKey('self', db_index = True, related_name = 'subscribed_tenants', null = True, blank = True )
  subscriber_user = ForeignKey(User, db_index = True, related_name = 'subscribed_tenants', null = True, blank = True )
  subscriber_root = ForeignKey(TenantRoot, db_index = True, related_name = 'subscribed_tenants', null = True, blank = True )
  subscriber_network = ForeignKey(Network, db_index = True, related_name = 'subscribed_tenants', null = True, blank = True )

  KIND="generic"
  
  def __init__(self, *args, **kwargs):
      # for subclasses, set the default kind appropriately
      self._meta.get_field("kind").default = self.KIND
      super(Tenant, self).__init__(*args, **kwargs)
  
  def __unicode__(self):
      return u"%s-tenant-%s" % (str(self.kind), str(self.id))
  
  @classmethod
  def get_tenant_objects(cls):
      return cls.objects.filter(kind=cls.KIND)
  
  @classmethod
  def get_tenant_objects_by_user(cls, user):
      return cls.select_by_user(user).filter(kind=cls.KIND)
  
  @classmethod
  def get_deleted_tenant_objects(cls):
      return cls.deleted_objects.filter(kind=cls.KIND)
  
  @property
  def tenantattribute_dict(self):
      attrs = {}
      for attr in self.tenantattributes.all():
          attrs[attr.name] = attr.value
      return attrs
  
  # helper function to be used in subclasses that want to ensure
  # service_specific_id is unique
  def validate_unique_service_specific_id(self):
      if self.pk is None:
          if self.service_specific_id is None:
              raise XOSMissingField("subscriber_specific_id is None, and it's a required field", fields={
                                    "service_specific_id": "cannot be none"})
  
          conflicts = self.get_tenant_objects().filter(
              service_specific_id=self.service_specific_id)
          if conflicts:
              raise XOSDuplicateKey("service_specific_id %s already exists" % self.service_specific_id, fields={
                                    "service_specific_id": "duplicate key"})
  
  def save(self, *args, **kwargs):
      subCount = sum([1 for e in [self.subscriber_service, self.subscriber_tenant,
                                  self.subscriber_user, self.subscriber_root] if e is not None])
      if (subCount > 1):
          raise XOSConflictingField(
              "Only one of subscriber_service, subscriber_tenant, subscriber_user, subscriber_root should be set")
  
      super(Tenant, self).save(*args, **kwargs)
  
  def get_subscribed_tenants(self, tenant_class):
      ids = self.subscribed_tenants.filter(kind=tenant_class.KIND)
      return tenant_class.objects.filter(id__in=ids)
  
  def get_newest_subscribed_tenant(self, kind):
      st = list(self.get_subscribed_tenants(kind))
      if not st:
          return None
      return sorted(st, key=attrgetter('id'))[0]
  
  pass

