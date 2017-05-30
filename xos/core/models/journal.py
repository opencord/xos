from __future__ import absolute_import

from django.db import models
from django.utils import timezone

from xos.exceptions import *
from operator import attrgetter
import json

class JournalEntry(models.Model):
    objClassName = models.CharField(max_length=64)
    objId = models.CharField(max_length=64, null=True, blank=True)  # null=True, for objects journaled before save
    objUnicode = models.CharField(max_length=1024)
    operation = models.CharField(max_length=64)
    msg = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __unicode__(self): return u'%s' % (self.name)

    def can_update(self, user):
        return True
