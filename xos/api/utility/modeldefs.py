from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_framework import generics
from rest_framework.exceptions import APIException
from xos.apibase import XOSListCreateAPIView, XOSRetrieveUpdateDestroyAPIView, XOSPermissionDenied
import json
from core.models import UserDashboardView, DashboardView
from api.xosapi_helpers import XOSViewSet, PlusModelSerializer
import django.apps
from rest_framework.views import APIView


class ModelDefsList(APIView):
    method_kind = "list"
    method_name = "modeldefs"

    def get(self, request, format=None):
        models = django.apps.apps.get_models()

        response = []

        for model in models:
            if 'core' in model.__module__:
                modeldef = {}
                modeldef['name'] = model.__name__

                fields = []
                relations = []
                for f in model._meta.fields:
                    fields.append({
                        'name': f.name,
                        'type': f.get_internal_type()
                    })

                    if f.is_relation and f.related_model:
                        relations.append(f.related_model.__name__)

                modeldef['fields'] = fields
                modeldef['relations'] = list(set(relations))
                response.append(modeldef)
        return Response(response)
