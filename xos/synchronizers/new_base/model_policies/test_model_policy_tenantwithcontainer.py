import unittest
from mock import patch
import mock

import os
config = basic_conf = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/test_config.yaml")
from xosconfig import Config
Config.init(config, 'synchronizer-config-schema.yaml')

from model_policy_tenantwithcontainer import TenantWithContainerPolicy


class MockTenant:
    provider_service = None
    def __init__(self):
        self.deleted = False
        self.instance = None
    pass

class TestModelPolicyTenantWithContainer(unittest.TestCase):

    def setUp(self):
        self.twc_policy = TenantWithContainerPolicy()

    def test_base(self):
        self.assertEqual(1, 1)

    @patch.object(TenantWithContainerPolicy, "get_image", wrap=TenantWithContainerPolicy.get_image)
    @patch.object(MockTenant, "provider_service")
    def test_manage_container(self, get_image, provider_service):
        tenant = MockTenant()
        get_image.return_value = 'image'
        provider_service.return_value.slices.return_value.count.return_value = 20
        self.twc_policy.manage_container(tenant)