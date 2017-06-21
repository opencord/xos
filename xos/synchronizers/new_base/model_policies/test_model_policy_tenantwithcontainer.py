import unittest
from mock import patch
import mock

import os, sys
sys.path.append("../../..")
sys.path.append("../../new_base/model_policies")
config = basic_conf = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/test_config.yaml")
from xosconfig import Config
Config.init(config, 'synchronizer-config-schema.yaml')

import synchronizers.new_base.modelaccessor

from model_policy_tenantwithcontainer import TenantWithContainerPolicy

class MockDeployment:
    name = None
    def __init__(self, **kwars):
        for (k,v) in kwargs:
            setattr(self,k,v)

class MockUser:
    email = None
    def __init__(self, **kwars):
        for (k,v) in kwargs:
            setattr(self,k,v)

class MockSlice:
    name = None
    def __init__(self, **kwars):
        for (k,v) in kwargs:
            setattr(self,k,v)

class MockNode:
    hostname = None
    def __init__(self, **kwars):
        for (k,v) in kwargs:
            setattr(self,k,v)

class MockImage:
    name = None
    def __init__(self, **kwars):
        for (k,v) in kwargs:
            setattr(self,k,v)

class MockTenant:
    provider_service = None
    deleted = False
    instance = None
    creator = None
    service_specific_attribute = {}

    def __init__(self, **kwars):
        for (k,v) in kwargs:
            setattr(self,k,v)

class TestModelPolicyVsgTenant(unittest.TestCase):
    def setUp(self):
        self.policy = TenantWithContainerPolicy()
        self.user = MockUser(email="testadmin@test.org")
        self.tenant = MockTenant(creator=user)

    @patch.object(MockTenant, "provider_service")
    def test_manage_container_no_slices(self, provider_service):
        provider_service.slices.count.return_value = 0
        with self.assertRaises(Exception) as e:
            self.policy.manage_container(self.tenant)
        self.assertEqual(e.exception.message, "The service has no slices")

    @patch.object(MockTenant, "provider_service")
    @patch.object(MockTenant, "get_image")
    @patch.object(LeastLoadedNodeScheduler, "pick")
    @patch.object(MockNode, "site_deployment")
    def test_manage_container(self, site_deployment, pick, get_image, provider_service):
        # setup mocks
        node = MockNode(hostname="my.node.com")
        slice = MockSlice(name="mysite_test1", default_flavor="m1.small", default_isolation="vm")
        image = MockImage(name="trusty-server-multi-nic")
        deployment = MockDeployment(name="testdeployment")
        provider_service.slices.count.return_value = 0
        provider_service.slices.all.return_value = [slice]
        provider_service.slices.first.return_value = slice
        get_image.return_value = image
        pick.return_value = node
        site_deployment.deployment = deployment
        # done setup mocks
        pdb.set_trace()
        self.policy.manage_containert(self.tenant)

if __name__ == '__main__':
    unittest.main()
