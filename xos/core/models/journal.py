from django.db import models
from core.models import PlCoreBase,SingletonModel,PlCoreBaseManager,User
from core.models.plcorebase import StrippedCharField
from xos.exceptions import *
from operator import attrgetter
import json

class JournalEntry(PlCoreBase):
    objClassName = StrippedCharField(max_length=32)
    objId = StrippedCharField(max_length=32)
    objUnicode = StrippedCharField(max_length=1024)
    operation = StrippedCharField(max_length=32)
    msg = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    name = StrippedCharField(max_length=30, help_text="Service Name")
    description = models.TextField(max_length=254,null=True, blank=True,help_text="Description of Service")
    kind = StrippedCharField(max_length=30, help_text="Kind of service", choices=KIND_CHOICES)
    command = StrippedCharField(blank=True, null=True, max_length=30, help_text="Command to run", choices=COMMAND_CHOICES)

    def __unicode__(self): return u'%s' % (self.name)

    def can_update(self, user):
        return True


def journal_object(o, operation, msg=None, timestamp=None):
    if not timestamp:
        timestamp = timezone.now()

    j = JournalEntry(objClassName = o.__class__.__name__,
                     objId = o.id,
                     objUnicode = str(o),
                     operation = operation,
                     msg= msg)
    j.save()



