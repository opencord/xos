from header import *

class Project(PlCoreBase):
    name = StrippedCharField(max_length=200, unique=True, help_text="Name of Project")

    def __unicode__(self):  return u'%s' % (self.name)

