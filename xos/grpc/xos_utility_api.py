import base64
import time
from protos import utility_pb2
from google.protobuf.empty_pb2 import Empty

from importlib import import_module
from django.conf import settings
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore

from django.contrib.auth import authenticate as django_authenticate
import django.apps
from core.models import *
from xos.exceptions import *
from apihelper import XOSAPIHelperMixin

class UtilityService(utility_pb2.utilityServicer, XOSAPIHelperMixin):
    def __init__(self, thread_pool):
        self.thread_pool = thread_pool

    def stop(self):
        pass

    def Login(self, request, context):
        u=django_authenticate(username=request.username, password=request.password)
        if not u:
            raise XOSPermissionDenied("Failed to authenticate user %s" % username)

        session = SessionStore()
        auth = {"username": request.username, "password": request.password}
        session["auth"] = auth
        session['_auth_user_id'] = u.pk
        session['_auth_user_backend'] = u.backend
        session.save()

        response = utility_pb2.LoginResponse()
        response.sessionid = session.session_key

        return response

