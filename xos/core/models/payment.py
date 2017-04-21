
from header import *





from core.models.account import Account 






class Payment(PlCoreBase):
  # Primitive Fields (Not Relations)
  amount = FloatField( default = 0.0, null = False, blank = False, db_index = False )
  date = DateTimeField( default = now, null = False, db_index = False, blank = False )
  

  # Relations
  
  account = ForeignKey(Account, db_index = True, related_name = 'payments', null = False, blank = False )

  def __unicode__(self): return u'%s-%0.2f-%s' % (self.account.site.name, self.amount, str(self.date))
  pass

