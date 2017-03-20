from header import *

class ServiceClass(PlCoreBase):
    name = StrippedCharField(max_length=32)
    description = StrippedCharField(max_length=255)
    commitment = models.IntegerField(default=365)
    membershipFee = models.IntegerField(default=0)
    membershipFeeMonths = models.IntegerField(default=12)
    upgradeRequiresApproval = models.BooleanField(default=False)
    upgradeFrom = models.ManyToManyField('self', blank=True)

    class Meta(PlCoreBase.Meta):
       verbose_name_plural = "Service classes"

    def __unicode__(self):  return u'%s' % (self.name)

    def save_by_user(self, user, *args, **kwds):
        if self.can_update(user):
            super(ServiceClass, self).save(*args, **kwds)
