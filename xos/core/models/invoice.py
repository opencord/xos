
from header import *





from core.models.account import Account 






class Invoice(PlCoreBase):
  # Primitive Fields (Not Relations)
  date = DateTimeField( blank = False, null = False, db_index = False )
  

  # Relations
  
  account = ForeignKey(Account, db_index = True, related_name = 'invoices', null = False, blank = False )

  @property
  def amount(self):
      return str(self.charges.all().aggregate(Sum('amount'))["amount__sum"])
  
  def __unicode__(self):  return u'%s-%s' % (self.account.site.name, str(self.date))
  pass

