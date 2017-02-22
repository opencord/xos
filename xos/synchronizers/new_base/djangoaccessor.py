import django.apps
from django.db import reset_queries
from django.utils import timezone
from modelaccessor import ModelAccessor
from diag import update_diag
from django.db import connection
from django import setup as django_setup # django 1.7

class DjangoModelAccessor(object):
    def __init__(self):
        super(DjangoModelAccessor, self).__init__()
        django_setup()

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

    def connection_close(self):
        connection.close()

    def check_db_connection_okay(self):
        # django implodes if the database connection is closed by
        # docker-compose
        try:
            diag = Diag.objects.filter(name="foo").first()
        except Exception as e:
            from django import db
            if "connection already closed" in traceback.format_exc():
                # logger.error("XXX connection already closed")
                try:
                    #                       if db.connection:
                    #                           db.connection.close()
                    db.close_old_connections()
                except:
                    pass #logger.log_exc("XXX we failed to fix the failure")
            else:
                pass #logger.log_exc("XXX some other error")

    def obj_exists(self, o):
        return (o.pk is not None)

    def obj_in_list(self, o, olist):
        return o in olist

    def now(self):
        return timezone.now()

    def update_diag(self, loop_end=None, loop_start=None, syncrecord_start=None, sync_start=None, backend_status=None):
        return update_diag(loop_end, loop_start, syncrecord_Start, sync_start, backend_status)

    def is_type(self, obj, name):
        return type(obj) == self.get_model_class(name)

    def is_type(self, obj, name):
        return isinstance(obj, self.get_model_class(name))


