
from header import *





from core.models.account import Account 



from core.models.slice import Slice 



from core.models.usableobject import UsableObject 



from core.models.invoice import Invoice 






class Charge(PlCoreBase):
  # Primitive Fields (Not Relations)
  kind = StrippedCharField( default = "besteffort", choices = (('besteffort', 'besteffort'), ('reservation', 'reservation'), ('monthlyfee', 'monthlyfee')), max_length = 30, blank = False, null = False, db_index = False )
  state = StrippedCharField( default = "pending", choices = (('pending', 'pending'), ('invoiced', 'invoiced')), max_length = 30, blank = False, null = False, db_index = False )
  date = DateTimeField( blank = False, null = False, db_index = False )
  amount = FloatField( default = 0.0, null = False, blank = False, db_index = False )
  coreHours = FloatField( default = 0.0, null = False, blank = False, db_index = False )
  

  # Relations
  
  account = ForeignKey(Account, db_index = True, related_name = 'charges', null = False, blank = False )
  slice = ForeignKey(Slice, db_index = True, related_name = 'charges', null = True, blank = True )
  object = ForeignKey(UsableObject, db_index = True, related_name = 'charge', null = False, blank = False )
  invoice = ForeignKey(Invoice, db_index = True, related_name = 'charges', null = True, blank = True )

  def __unicode__(self):  return u'%s-%0.2f-%s' % (self.account.site.name, self.amount, str(self.date))
  pass

