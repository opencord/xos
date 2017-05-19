

from service_header import *



from core.models.serviceclass import ServiceClass 






class ServiceResource(XOSBase):
  # Primitive Fields (Not Relations)
  name = StrippedCharField( db_index = False, max_length = 32, null = False, blank = False )
  maxUnitsDeployment = IntegerField( default = 1, null = False, blank = False, db_index = False )
  maxUnitsNode = IntegerField( default = 1, null = False, blank = False, db_index = False )
  maxDuration = IntegerField( default = 1, null = False, blank = False, db_index = False )
  bucketInRate = IntegerField( default = 0, null = False, blank = False, db_index = False )
  bucketMaxSize = IntegerField( default = 0, null = False, blank = False, db_index = False )
  cost = IntegerField( default = 0, null = False, blank = False, db_index = False )
  calendarReservable = BooleanField( default = True, null = False, blank = True, db_index = False )
  

  # Relations
  
  serviceClass = ForeignKey(ServiceClass, db_index = True, related_name = 'serviceresources', null = False, blank = False )

  def __unicode__(self):  return u'%s' % (self.name)
  pass

