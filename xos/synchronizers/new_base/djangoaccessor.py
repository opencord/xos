import django.apps
from django.db import reset_queries
from django.utils import timezone
from modelaccessor import ModelAccessor

class DjangoModelAccessor(object):
    def __init__(self):
        super(DjangoModelAccessor, self).__init__()

    def get_all_model_classes(self):
        self.all_model_classes = {}
        for model in django.apps.apps.get_models():
            self.all_model_classes[model.__name__] = model

    def fetch_pending(self, names, deletion=False):
        objs = []
        for name in names:
            mc = self.get_model_class(name)
            if (not deletion):
                lobjs = mc.objects.filter(Q(enacted__lt=F('updated')) | Q(enacted=None),Q(lazy_blocked=False),Q(no_sync=False))
            else:
                lobjs = mc.deleted_objects.all()
            objs.extend(lobjs)

    def reset_queries(self):
        reset_queries()

    def obj_exists(self, o):
        return (o.pk is not None)

    def obj_in_list(self, o, olist):
        return o in olist

    def now(self):
        return timezone.now()
