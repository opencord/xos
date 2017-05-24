import base64
import time
from protos import xos_pb2
from google.protobuf.empty_pb2 import Empty

from django.contrib.auth import authenticate as django_authenticate
from xos.exceptions import *
from apihelper import XOSAPIHelperMixin, translate_exceptions

class XosService(xos_pb2.xosServicer, XOSAPIHelperMixin):
    def __init__(self, thread_pool):
        self.thread_pool = thread_pool
        XOSAPIHelperMixin.__init__(self)

    def stop(self):
        pass


    @translate_exceptions
    def ListAccessAgent(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AccessAgent")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterAccessAgent(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AccessAgent")
      return self.filter(model, request)

    @translate_exceptions
    def GetAccessAgent(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AccessAgent")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateAccessAgent(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AccessAgent")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteAccessAgent(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AccessAgent")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateAccessAgent(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AccessAgent")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListAccessDevice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AccessDevice")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterAccessDevice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AccessDevice")
      return self.filter(model, request)

    @translate_exceptions
    def GetAccessDevice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AccessDevice")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateAccessDevice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AccessDevice")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteAccessDevice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AccessDevice")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateAccessDevice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AccessDevice")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListAddressPool(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AddressPool")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterAddressPool(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AddressPool")
      return self.filter(model, request)

    @translate_exceptions
    def GetAddressPool(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AddressPool")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateAddressPool(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AddressPool")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteAddressPool(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AddressPool")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateAddressPool(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AddressPool")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListAgentPortMapping(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AgentPortMapping")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterAgentPortMapping(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AgentPortMapping")
      return self.filter(model, request)

    @translate_exceptions
    def GetAgentPortMapping(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AgentPortMapping")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateAgentPortMapping(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AgentPortMapping")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteAgentPortMapping(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AgentPortMapping")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateAgentPortMapping(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("AgentPortMapping")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListController(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Controller")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterController(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Controller")
      return self.filter(model, request)

    @translate_exceptions
    def GetController(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Controller")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateController(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Controller")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteController(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Controller")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateController(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Controller")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListControllerDashboardView(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerDashboardView")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterControllerDashboardView(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerDashboardView")
      return self.filter(model, request)

    @translate_exceptions
    def GetControllerDashboardView(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerDashboardView")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateControllerDashboardView(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerDashboardView")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteControllerDashboardView(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerDashboardView")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateControllerDashboardView(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerDashboardView")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListControllerImages(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerImages")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterControllerImages(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerImages")
      return self.filter(model, request)

    @translate_exceptions
    def GetControllerImages(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerImages")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateControllerImages(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerImages")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteControllerImages(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerImages")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateControllerImages(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerImages")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListControllerNetwork(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerNetwork")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterControllerNetwork(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerNetwork")
      return self.filter(model, request)

    @translate_exceptions
    def GetControllerNetwork(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerNetwork")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateControllerNetwork(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerNetwork")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteControllerNetwork(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerNetwork")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateControllerNetwork(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerNetwork")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListControllerRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerRole")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterControllerRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerRole")
      return self.filter(model, request)

    @translate_exceptions
    def GetControllerRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerRole")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateControllerRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerRole")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteControllerRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerRole")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateControllerRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerRole")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListControllerSite(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSite")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterControllerSite(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSite")
      return self.filter(model, request)

    @translate_exceptions
    def GetControllerSite(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSite")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateControllerSite(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSite")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteControllerSite(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSite")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateControllerSite(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSite")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListControllerSitePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSitePrivilege")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterControllerSitePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSitePrivilege")
      return self.filter(model, request)

    @translate_exceptions
    def GetControllerSitePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSitePrivilege")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateControllerSitePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSitePrivilege")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteControllerSitePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSitePrivilege")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateControllerSitePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSitePrivilege")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListControllerSlice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSlice")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterControllerSlice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSlice")
      return self.filter(model, request)

    @translate_exceptions
    def GetControllerSlice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSlice")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateControllerSlice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSlice")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteControllerSlice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSlice")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateControllerSlice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSlice")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListControllerSlicePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSlicePrivilege")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterControllerSlicePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSlicePrivilege")
      return self.filter(model, request)

    @translate_exceptions
    def GetControllerSlicePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSlicePrivilege")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateControllerSlicePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSlicePrivilege")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteControllerSlicePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSlicePrivilege")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateControllerSlicePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerSlicePrivilege")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListControllerUser(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerUser")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterControllerUser(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerUser")
      return self.filter(model, request)

    @translate_exceptions
    def GetControllerUser(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerUser")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateControllerUser(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerUser")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteControllerUser(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerUser")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateControllerUser(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ControllerUser")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListCordSubscriberRoot(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("CordSubscriberRoot")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterCordSubscriberRoot(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("CordSubscriberRoot")
      return self.filter(model, request)

    @translate_exceptions
    def GetCordSubscriberRoot(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("CordSubscriberRoot")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateCordSubscriberRoot(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("CordSubscriberRoot")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteCordSubscriberRoot(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("CordSubscriberRoot")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateCordSubscriberRoot(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("CordSubscriberRoot")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListDashboardView(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("DashboardView")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterDashboardView(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("DashboardView")
      return self.filter(model, request)

    @translate_exceptions
    def GetDashboardView(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("DashboardView")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateDashboardView(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("DashboardView")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteDashboardView(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("DashboardView")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateDashboardView(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("DashboardView")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListDeployment(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Deployment")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterDeployment(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Deployment")
      return self.filter(model, request)

    @translate_exceptions
    def GetDeployment(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Deployment")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateDeployment(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Deployment")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteDeployment(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Deployment")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateDeployment(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Deployment")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListDeploymentPrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("DeploymentPrivilege")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterDeploymentPrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("DeploymentPrivilege")
      return self.filter(model, request)

    @translate_exceptions
    def GetDeploymentPrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("DeploymentPrivilege")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateDeploymentPrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("DeploymentPrivilege")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteDeploymentPrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("DeploymentPrivilege")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateDeploymentPrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("DeploymentPrivilege")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListDeploymentRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("DeploymentRole")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterDeploymentRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("DeploymentRole")
      return self.filter(model, request)

    @translate_exceptions
    def GetDeploymentRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("DeploymentRole")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateDeploymentRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("DeploymentRole")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteDeploymentRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("DeploymentRole")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateDeploymentRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("DeploymentRole")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListDiag(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Diag")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterDiag(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Diag")
      return self.filter(model, request)

    @translate_exceptions
    def GetDiag(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Diag")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateDiag(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Diag")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteDiag(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Diag")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateDiag(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Diag")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListExampleService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ExampleService")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterExampleService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ExampleService")
      return self.filter(model, request)

    @translate_exceptions
    def GetExampleService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ExampleService")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateExampleService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ExampleService")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteExampleService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ExampleService")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateExampleService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ExampleService")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListExampleTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ExampleTenant")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterExampleTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ExampleTenant")
      return self.filter(model, request)

    @translate_exceptions
    def GetExampleTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ExampleTenant")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateExampleTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ExampleTenant")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteExampleTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ExampleTenant")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateExampleTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ExampleTenant")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListFabricService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("FabricService")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterFabricService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("FabricService")
      return self.filter(model, request)

    @translate_exceptions
    def GetFabricService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("FabricService")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateFabricService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("FabricService")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteFabricService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("FabricService")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateFabricService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("FabricService")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListFlavor(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Flavor")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterFlavor(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Flavor")
      return self.filter(model, request)

    @translate_exceptions
    def GetFlavor(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Flavor")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateFlavor(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Flavor")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteFlavor(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Flavor")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateFlavor(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Flavor")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListImage(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Image")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterImage(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Image")
      return self.filter(model, request)

    @translate_exceptions
    def GetImage(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Image")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateImage(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Image")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteImage(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Image")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateImage(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Image")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListImageDeployments(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ImageDeployments")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterImageDeployments(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ImageDeployments")
      return self.filter(model, request)

    @translate_exceptions
    def GetImageDeployments(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ImageDeployments")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateImageDeployments(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ImageDeployments")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteImageDeployments(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ImageDeployments")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateImageDeployments(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ImageDeployments")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListInstance(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Instance")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterInstance(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Instance")
      return self.filter(model, request)

    @translate_exceptions
    def GetInstance(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Instance")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateInstance(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Instance")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteInstance(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Instance")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateInstance(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Instance")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListNetwork(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Network")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterNetwork(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Network")
      return self.filter(model, request)

    @translate_exceptions
    def GetNetwork(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Network")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateNetwork(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Network")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteNetwork(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Network")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateNetwork(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Network")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListNetworkParameter(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkParameter")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterNetworkParameter(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkParameter")
      return self.filter(model, request)

    @translate_exceptions
    def GetNetworkParameter(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkParameter")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateNetworkParameter(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkParameter")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteNetworkParameter(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkParameter")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateNetworkParameter(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkParameter")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListNetworkParameterType(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkParameterType")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterNetworkParameterType(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkParameterType")
      return self.filter(model, request)

    @translate_exceptions
    def GetNetworkParameterType(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkParameterType")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateNetworkParameterType(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkParameterType")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteNetworkParameterType(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkParameterType")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateNetworkParameterType(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkParameterType")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListNetworkSlice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkSlice")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterNetworkSlice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkSlice")
      return self.filter(model, request)

    @translate_exceptions
    def GetNetworkSlice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkSlice")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateNetworkSlice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkSlice")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteNetworkSlice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkSlice")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateNetworkSlice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkSlice")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListNetworkTemplate(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkTemplate")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterNetworkTemplate(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkTemplate")
      return self.filter(model, request)

    @translate_exceptions
    def GetNetworkTemplate(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkTemplate")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateNetworkTemplate(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkTemplate")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteNetworkTemplate(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkTemplate")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateNetworkTemplate(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NetworkTemplate")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListNode(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Node")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterNode(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Node")
      return self.filter(model, request)

    @translate_exceptions
    def GetNode(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Node")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateNode(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Node")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteNode(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Node")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateNode(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Node")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListNodeLabel(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NodeLabel")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterNodeLabel(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NodeLabel")
      return self.filter(model, request)

    @translate_exceptions
    def GetNodeLabel(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NodeLabel")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateNodeLabel(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NodeLabel")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteNodeLabel(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NodeLabel")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateNodeLabel(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("NodeLabel")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListONOSApp(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ONOSApp")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterONOSApp(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ONOSApp")
      return self.filter(model, request)

    @translate_exceptions
    def GetONOSApp(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ONOSApp")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateONOSApp(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ONOSApp")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteONOSApp(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ONOSApp")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateONOSApp(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ONOSApp")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListONOSService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ONOSService")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterONOSService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ONOSService")
      return self.filter(model, request)

    @translate_exceptions
    def GetONOSService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ONOSService")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateONOSService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ONOSService")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteONOSService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ONOSService")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateONOSService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ONOSService")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListPort(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Port")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterPort(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Port")
      return self.filter(model, request)

    @translate_exceptions
    def GetPort(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Port")
      return self.get(model, request.id)

    @translate_exceptions
    def CreatePort(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Port")
      return self.create(model, user, request)

    @translate_exceptions
    def DeletePort(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Port")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdatePort(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Port")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Role")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Role")
      return self.filter(model, request)

    @translate_exceptions
    def GetRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Role")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Role")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Role")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Role")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Service")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Service")
      return self.filter(model, request)

    @translate_exceptions
    def GetService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Service")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Service")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Service")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Service")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListServiceAttribute(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceAttribute")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterServiceAttribute(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceAttribute")
      return self.filter(model, request)

    @translate_exceptions
    def GetServiceAttribute(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceAttribute")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateServiceAttribute(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceAttribute")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteServiceAttribute(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceAttribute")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateServiceAttribute(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceAttribute")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListServiceDependency(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceDependency")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterServiceDependency(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceDependency")
      return self.filter(model, request)

    @translate_exceptions
    def GetServiceDependency(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceDependency")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateServiceDependency(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceDependency")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteServiceDependency(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceDependency")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateServiceDependency(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceDependency")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListServiceMonitoringAgentInfo(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceMonitoringAgentInfo")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterServiceMonitoringAgentInfo(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceMonitoringAgentInfo")
      return self.filter(model, request)

    @translate_exceptions
    def GetServiceMonitoringAgentInfo(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceMonitoringAgentInfo")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateServiceMonitoringAgentInfo(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceMonitoringAgentInfo")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteServiceMonitoringAgentInfo(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceMonitoringAgentInfo")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateServiceMonitoringAgentInfo(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceMonitoringAgentInfo")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListServicePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServicePrivilege")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterServicePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServicePrivilege")
      return self.filter(model, request)

    @translate_exceptions
    def GetServicePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServicePrivilege")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateServicePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServicePrivilege")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteServicePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServicePrivilege")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateServicePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServicePrivilege")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListServiceRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceRole")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterServiceRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceRole")
      return self.filter(model, request)

    @translate_exceptions
    def GetServiceRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceRole")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateServiceRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceRole")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteServiceRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceRole")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateServiceRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("ServiceRole")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListSite(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Site")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterSite(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Site")
      return self.filter(model, request)

    @translate_exceptions
    def GetSite(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Site")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateSite(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Site")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteSite(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Site")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateSite(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Site")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListSiteDeployment(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SiteDeployment")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterSiteDeployment(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SiteDeployment")
      return self.filter(model, request)

    @translate_exceptions
    def GetSiteDeployment(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SiteDeployment")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateSiteDeployment(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SiteDeployment")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteSiteDeployment(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SiteDeployment")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateSiteDeployment(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SiteDeployment")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListSitePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SitePrivilege")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterSitePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SitePrivilege")
      return self.filter(model, request)

    @translate_exceptions
    def GetSitePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SitePrivilege")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateSitePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SitePrivilege")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteSitePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SitePrivilege")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateSitePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SitePrivilege")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListSiteRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SiteRole")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterSiteRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SiteRole")
      return self.filter(model, request)

    @translate_exceptions
    def GetSiteRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SiteRole")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateSiteRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SiteRole")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteSiteRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SiteRole")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateSiteRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SiteRole")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListSlice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Slice")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterSlice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Slice")
      return self.filter(model, request)

    @translate_exceptions
    def GetSlice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Slice")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateSlice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Slice")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteSlice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Slice")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateSlice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Slice")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListSlicePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SlicePrivilege")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterSlicePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SlicePrivilege")
      return self.filter(model, request)

    @translate_exceptions
    def GetSlicePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SlicePrivilege")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateSlicePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SlicePrivilege")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteSlicePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SlicePrivilege")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateSlicePrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SlicePrivilege")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListSliceRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SliceRole")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterSliceRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SliceRole")
      return self.filter(model, request)

    @translate_exceptions
    def GetSliceRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SliceRole")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateSliceRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SliceRole")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteSliceRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SliceRole")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateSliceRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("SliceRole")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListTag(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Tag")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterTag(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Tag")
      return self.filter(model, request)

    @translate_exceptions
    def GetTag(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Tag")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateTag(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Tag")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteTag(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Tag")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateTag(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Tag")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Tenant")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Tenant")
      return self.filter(model, request)

    @translate_exceptions
    def GetTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Tenant")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Tenant")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Tenant")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("Tenant")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListTenantAttribute(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantAttribute")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterTenantAttribute(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantAttribute")
      return self.filter(model, request)

    @translate_exceptions
    def GetTenantAttribute(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantAttribute")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateTenantAttribute(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantAttribute")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteTenantAttribute(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantAttribute")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateTenantAttribute(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantAttribute")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListTenantPrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantPrivilege")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterTenantPrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantPrivilege")
      return self.filter(model, request)

    @translate_exceptions
    def GetTenantPrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantPrivilege")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateTenantPrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantPrivilege")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteTenantPrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantPrivilege")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateTenantPrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantPrivilege")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListTenantRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRole")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterTenantRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRole")
      return self.filter(model, request)

    @translate_exceptions
    def GetTenantRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRole")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateTenantRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRole")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteTenantRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRole")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateTenantRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRole")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListTenantRoot(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRoot")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterTenantRoot(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRoot")
      return self.filter(model, request)

    @translate_exceptions
    def GetTenantRoot(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRoot")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateTenantRoot(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRoot")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteTenantRoot(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRoot")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateTenantRoot(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRoot")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListTenantRootPrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRootPrivilege")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterTenantRootPrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRootPrivilege")
      return self.filter(model, request)

    @translate_exceptions
    def GetTenantRootPrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRootPrivilege")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateTenantRootPrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRootPrivilege")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteTenantRootPrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRootPrivilege")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateTenantRootPrivilege(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRootPrivilege")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListTenantRootRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRootRole")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterTenantRootRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRootRole")
      return self.filter(model, request)

    @translate_exceptions
    def GetTenantRootRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRootRole")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateTenantRootRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRootRole")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteTenantRootRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRootRole")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateTenantRootRole(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantRootRole")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListTenantWithContainer(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantWithContainer")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterTenantWithContainer(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantWithContainer")
      return self.filter(model, request)

    @translate_exceptions
    def GetTenantWithContainer(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantWithContainer")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateTenantWithContainer(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantWithContainer")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteTenantWithContainer(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantWithContainer")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateTenantWithContainer(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("TenantWithContainer")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListUser(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("User")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterUser(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("User")
      return self.filter(model, request)

    @translate_exceptions
    def GetUser(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("User")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateUser(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("User")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteUser(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("User")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateUser(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("User")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListVOLTDevice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VOLTDevice")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterVOLTDevice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VOLTDevice")
      return self.filter(model, request)

    @translate_exceptions
    def GetVOLTDevice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VOLTDevice")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateVOLTDevice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VOLTDevice")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteVOLTDevice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VOLTDevice")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateVOLTDevice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VOLTDevice")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListVOLTService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VOLTService")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterVOLTService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VOLTService")
      return self.filter(model, request)

    @translate_exceptions
    def GetVOLTService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VOLTService")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateVOLTService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VOLTService")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteVOLTService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VOLTService")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateVOLTService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VOLTService")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListVOLTTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VOLTTenant")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterVOLTTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VOLTTenant")
      return self.filter(model, request)

    @translate_exceptions
    def GetVOLTTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VOLTTenant")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateVOLTTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VOLTTenant")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteVOLTTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VOLTTenant")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateVOLTTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VOLTTenant")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListVRouterApp(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterApp")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterVRouterApp(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterApp")
      return self.filter(model, request)

    @translate_exceptions
    def GetVRouterApp(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterApp")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateVRouterApp(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterApp")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteVRouterApp(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterApp")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateVRouterApp(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterApp")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListVRouterDevice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterDevice")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterVRouterDevice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterDevice")
      return self.filter(model, request)

    @translate_exceptions
    def GetVRouterDevice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterDevice")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateVRouterDevice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterDevice")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteVRouterDevice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterDevice")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateVRouterDevice(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterDevice")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListVRouterInterface(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterInterface")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterVRouterInterface(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterInterface")
      return self.filter(model, request)

    @translate_exceptions
    def GetVRouterInterface(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterInterface")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateVRouterInterface(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterInterface")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteVRouterInterface(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterInterface")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateVRouterInterface(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterInterface")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListVRouterIp(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterIp")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterVRouterIp(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterIp")
      return self.filter(model, request)

    @translate_exceptions
    def GetVRouterIp(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterIp")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateVRouterIp(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterIp")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteVRouterIp(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterIp")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateVRouterIp(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterIp")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListVRouterPort(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterPort")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterVRouterPort(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterPort")
      return self.filter(model, request)

    @translate_exceptions
    def GetVRouterPort(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterPort")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateVRouterPort(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterPort")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteVRouterPort(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterPort")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateVRouterPort(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterPort")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListVRouterService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterService")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterVRouterService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterService")
      return self.filter(model, request)

    @translate_exceptions
    def GetVRouterService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterService")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateVRouterService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterService")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteVRouterService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterService")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateVRouterService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterService")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListVRouterTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterTenant")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterVRouterTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterTenant")
      return self.filter(model, request)

    @translate_exceptions
    def GetVRouterTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterTenant")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateVRouterTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterTenant")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteVRouterTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterTenant")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateVRouterTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VRouterTenant")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListVSGService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VSGService")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterVSGService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VSGService")
      return self.filter(model, request)

    @translate_exceptions
    def GetVSGService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VSGService")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateVSGService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VSGService")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteVSGService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VSGService")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateVSGService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VSGService")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListVSGTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VSGTenant")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterVSGTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VSGTenant")
      return self.filter(model, request)

    @translate_exceptions
    def GetVSGTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VSGTenant")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateVSGTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VSGTenant")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteVSGTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VSGTenant")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateVSGTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VSGTenant")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListVTNService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VTNService")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterVTNService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VTNService")
      return self.filter(model, request)

    @translate_exceptions
    def GetVTNService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VTNService")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateVTNService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VTNService")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteVTNService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VTNService")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateVTNService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VTNService")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListVTRService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VTRService")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterVTRService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VTRService")
      return self.filter(model, request)

    @translate_exceptions
    def GetVTRService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VTRService")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateVTRService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VTRService")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteVTRService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VTRService")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateVTRService(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VTRService")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListVTRTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VTRTenant")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterVTRTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VTRTenant")
      return self.filter(model, request)

    @translate_exceptions
    def GetVTRTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VTRTenant")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateVTRTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VTRTenant")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteVTRTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VTRTenant")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateVTRTenant(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("VTRTenant")
      return self.update(model, user, request.id, request, context)

    @translate_exceptions
    def ListXOS(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("XOS")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterXOS(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("XOS")
      return self.filter(model, request)

    @translate_exceptions
    def GetXOS(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("XOS")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateXOS(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("XOS")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteXOS(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("XOS")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateXOS(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("XOS")
      return self.update(model, user, request.id, request, context)


    @translate_exceptions
    def ListXOSGuiExtension(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("XOSGuiExtension")
      return self.querysetToProto(model, model.objects.all())

    @translate_exceptions
    def FilterXOSGuiExtension(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("XOSGuiExtension")
      return self.filter(model, request)

    @translate_exceptions
    def GetXOSGuiExtension(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("XOSGuiExtension")
      return self.get(model, request.id)

    @translate_exceptions
    def CreateXOSGuiExtension(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("XOSGuiExtension")
      return self.create(model, user, request)

    @translate_exceptions
    def DeleteXOSGuiExtension(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("XOSGuiExtension")
      return self.delete(model, user, request.id)

    @translate_exceptions
    def UpdateXOSGuiExtension(self, request, context):
      user=self.authenticate(context)
      model=self.get_model("XOSGuiExtension")
      return self.update(model, user, request.id, request, context)


