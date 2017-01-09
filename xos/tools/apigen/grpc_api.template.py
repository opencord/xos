import time
from protos import xos_pb2

from core.models import *

class XosService(xos_pb2.xosServicer):
    def __init__(self, thread_pool):
        self.thread_pool = thread_pool

    def stop(self):
        pass

    def getProtoClass(self, djangoClass):
        pClass = getattr(xos_pb2, djangoClass.__name__)
        return pClass

    def getPluralProtoClass(self, djangoClass):
        pClass = getattr(xos_pb2, djangoClass.__name__ + "s")
        return pClass

    def convertFloat(self, x):
        if not x:
            return 0
        else:
            return float(x)

    def convertDateTime(self, x):
        if not x:
            return 0
        else:
            return time.mktime(x.timetuple())

    def convertForeignKey(self, x):
        if not x:
            return 0
        else:
            return int(x.id)

    def objToProto(self, obj):
        p_obj = self.getProtoClass(obj.__class__)()
        for field in obj._meta.fields:
            if getattr(obj, field.name) == None:
                # proto3 has no notion of a "null" field. All fields that are
                # not specified are assumed to be set to their defaults.
                #    string: ""
                #    integer: 0
                #    bool: False
                continue

            ftype = field.get_internal_type()
            if (ftype == "CharField") or (ftype == "TextField") or (ftype == "SlugField"):
                setattr(p_obj, field.name, str(getattr(obj, field.name)))
            elif (ftype == "BooleanField"):
                setattr(p_obj, field.name, getattr(obj, field.name))
            elif (ftype == "AutoField"):
                setattr(p_obj, field.name, int(getattr(obj, field.name)))
            elif (ftype == "IntegerField") or (ftype == "PositiveIntegerField"):
                setattr(p_obj, field.name, int(getattr(obj, field.name)))
            elif (ftype == "ForeignKey"):
                setattr(p_obj, field.name+"_id", self.convertForeignKey(getattr(obj, field.name)))
            elif (ftype == "DateTimeField"):
                setattr(p_obj, field.name, self.convertDateTime(getattr(obj, field.name)))
            elif (ftype == "FloatField"):
                setattr(p_obj, field.name, float(getattr(obj, field.name)))
            elif (ftype == "GenericIPAddressField"):
                setattr(p_obj, field.name, str(getattr(obj, field.name)))
        return p_obj

    def protoToArgs(self, djangoClass, message):
        args={}
        fmap={}
        fset={}
        for field in djangoClass._meta.fields:
            fmap[field.name] = field
            if field.get_internal_type() == "ForeignKey":
               # foreign key can be represented as an id
               fmap[field.name + "_id"] = field

        for (fieldDesc, val) in message.ListFields():
            name = fieldDesc.name
            if name in fmap:
                if (name=="id"):
                    # don't let anyone set the id
                    continue
                ftype = fmap[name].get_internal_type()
                if (ftype == "CharField") or (ftype == "TextField") or (ftype == "SlugField"):
                    args[name] = val
                elif (ftype == "BooleanField"):
                    args[name] = val
                elif (ftype == "AutoField"):
                    args[name] = val
                elif (ftype == "IntegerField") or (ftype == "PositiveIntegerField"):
                    args[name] = val
                elif (ftype == "ForeignKey"):
                    args[name] = val # field name already has "_id" at the end
                elif (ftype == "DateTimeField"):
                    pass # do something special here
                elif (ftype == "FloatField"):
                    args[name] = val
                elif (ftype == "GenericIPAddressField"):
                    args[name] = val
                fset[name] = True

        # proto3 has no notion of "null" fields for basic types. So we have to
        # assume anything not returned by ListFields() was set to the default
        # for that basic type.

        # TODO: consider proto2 instead of proto3.

#        for field in djangoClass._meta.fields:
#            if field.name=="id":
#                # never try to set an id to null
#                continue
#            name=field.name
#            if not fset.get(field.name, False):
#                ftype = field.get_internal_type()
#                if (ftype == "CharField") or (ftype == "TextField") or (ftype == "SlugField"):
#                    args[name] = ""
#                elif (ftype == "BooleanField"):
#                    args[name] = False
#                elif (ftype == "AutoField"):
#                    args[name] = 0
#                elif (ftype == "IntegerField") or (ftype == "PositiveIntegerField"):
#                    args[name] = 0
#                elif (ftype == "ForeignKey"):
#                    if not fset.get(field.name+"_id",False):
#                        args[name] = 0
#                elif (ftype == "DateTimeField"):
#                    pass # do something special here
#                elif (ftype == "FloatField"):
#                    args[name] = 0.0
#                elif (ftype == "GenericIPAddressField"):
#                    args[name] = ""

        return args

    def querysetToProto(self, djangoClass, queryset):
        objs = queryset
        p_objs = self.getPluralProtoClass(djangoClass)()

        for obj in objs:
           new_obj = p_objs.items.add()
           new_obj.CopyFrom(self.objToProto(obj))

        return p_objs

    def get(self, djangoClass, id):
        obj = djangoClass.objects.get(id=id)
        return self.objToProto(obj)

    def create(self, djangoClass, request):
        args = self.protoToArgs(djangoClass, request)
        new_obj = djangoClass(**args)
        import pdb
        pdb.set_trace()
        new_obj.save()
        return self.objToProto(new_obj)

{% for object in generator.all() %}
    def List{{ object.camel() }}(self, request, context):
      return self.querysetToProto({{ object.camel() }}, {{ object.camel() }}.objects.all())

    def Get{{ object.camel() }}(self, request, context):
      return self.get({{ object.camel() }}, request.id)

    def Create{{ object.camel() }}(self, request, context):
      return self.create({{ object.camel() }}, request)
{% endfor %}


