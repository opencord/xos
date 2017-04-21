def __unicode__(self):  return u'%s' % (self.name)

def __init__(self, *args, **kwargs):
    super(Node, self).__init__(*args, **kwargs)
    self.no_sync=True

def can_update(self, user):
    return user.can_update_site(self.site, allow=['tech'])

