""" ModelAccessor

    A class for abstracting access to models. Used to get any djangoisms out
    of the synchronizer code base.

    This module will import all models into its global scope, so doing a
    "from modelaccessor import *" from a calling module ought to import all
    models into the calling module's scope.
"""

class ModelAccessor(object):
    def __init__(self):
        self.all_model_classes = self.get_all_model_classes()

    def get_all_model_classes(self):
        """ Build a dictionary of all model class names """
        raise Exception("Not Implemented")

    def get_model_class(self, name):
        """ Given a class name, return that model class """
        return self.all_model_classes[name]

    def fetch_pending(self, name, deletion=False):
        """ Execute the default fetch_pending query """
        raise Exception("Not Implemented")

    def reset_queries(self):
        """ Reset any state between passes of synchronizer. For django, to
            limit memory consumption of cached queries.
        """
        pass

    def connection_close(self):
        """ Close any active database connection. For django, to limit memory
            consumption.
        """
        pass

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
        """ Return True if the object exists in the data model """
        raise Exception("Not Implemented")

    def obj_in_list(self, o, olist):
        """ Return True if o is the same as one of the objects in olist """
        raise Exception("Not Implemented")

    def now(self):
        """ Return the current time for timestamping purposes """
        raise Exception("Not Implemented")

    def update_diag(loop_end=None, loop_start=None, syncrecord_start=None, sync_start=None, backend_status=None):
        """ Update the diagnostic object """
        pass

    def is_type(self, obj, name):
        """ returns True is obj is of model type "name" """
        raise Exception("Not Implemented")

    def is_instance(self, obj, name):
        """ returns True if obj is of model type "name" or is a descendant """
        raise Exception("Not Implemented")


# TODO: insert logic here to pick accessor based on config setting
if True:
   from djangomodelaccessor import DjangoModelAccessor
   model_accessor = DjangoModelAccessor()
else:
   from apimodelaccessor import ApiModelAccessor
   model_accessor = ApiModelAccessor()

# add all models to globals
for (k, v) in model_accessor.all_model_classes():
    globals()[k] = v

# plcorebase doesn't exist from the synchronizer's perspective, so fake out
# ModelLink.
if "ModelLink" not in globals():
    class ModelLink:
        def __init__(self,dest,via,into=None):
            self.dest=dest
            self.via=via
            self.into=into
    globals()["ModelLink"] = ModelLink


