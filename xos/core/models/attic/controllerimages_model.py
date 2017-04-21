class Meta:
    unique_together = ('image', 'controller')
         
def __unicode__(self):  return u'%s %s' % (self.image, self.controller)
