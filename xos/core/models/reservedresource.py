
from header import *





from core.models.instance import Instance 



from core.models.serviceresource import ServiceResource 



from core.models.reservation import Reservation 






class ReservedResource(PlCoreBase):
  # Primitive Fields (Not Relations)
  quantity = IntegerField( default = 1, null = False, blank = False, db_index = False )
  

  # Relations
  
  instance = ForeignKey(Instance, db_index = True, related_name = 'reservedresources', null = False, blank = False )
  resource = ForeignKey(ServiceResource, db_index = True, related_name = 'reservedresources', null = False, blank = False )
  reservationSet = ForeignKey(Reservation, db_index = True, related_name = 'reservedresources', null = False, blank = False )

  class Meta(PlCoreBase.Meta):
     verbose_name_plural = "Reserved Resources"
  
  def __unicode__(self):  return u'%d %s on %s' % (self.quantity, self.resource, self.instance)
  
  def can_update(self, user):
      return user.can_update(self.instance.slice)
  
  @staticmethod
  def select_by_user(user):
      if user.is_admin:
          qs = ReservedResource.objects.all()
      else:
          instance_ids = [s.id for s in Instance.select_by_user(user)]
          qs = ReservedResource.objects.filter(id__in=instance_ids)
      return qs
  pass

