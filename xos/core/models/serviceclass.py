

from service_header import *








class ServiceClass(XOSBase):
  # Primitive Fields (Not Relations)
  name = StrippedCharField( db_index = False, max_length = 32, null = False, blank = False )
  description = StrippedCharField( db_index = False, max_length = 255, null = False, blank = False )
  commitment = IntegerField( default = 365, null = False, blank = False, db_index = False )
  membershipFee = IntegerField( default = 0, null = False, blank = False, db_index = False )
  membershipFeeMonths = IntegerField( default = 12, null = False, blank = False, db_index = False )
  upgradeRequiresApproval = BooleanField( default = False, null = False, blank = True, db_index = False )
  

  # Relations
  
  upgradeFrom = ManyToManyField('self', db_index = False, null = False, blank = True )

  class Meta(XOSBase.Meta):
     verbose_name_plural = "Service classes"
  
  def __unicode__(self):  return u'%s' % (self.name)
  
  def save_by_user(self, user, *args, **kwds):
      if self.can_update(user):
          super(ServiceClass, self).save(*args, **kwds)
  pass

