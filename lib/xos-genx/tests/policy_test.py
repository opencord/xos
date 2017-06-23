import unittest
from xosgenx.generator import XOSGenerator
from helpers import FakeArgs, XProtoTestHelpers

class XProtoPolicyTest(unittest.TestCase):
    def test_constant(self):
        xproto = \
"""
    policy true_policy < true >
"""

        target = XProtoTestHelpers.write_tmp_target("")

        args = FakeArgs()
        args.inputs = xproto
        args.target = target

        output = XOSGenerator.generate(args)

        self.assertTrue(True)

    def test_equal(self):
        xproto = \
"""
    policy slice_user < slice.user = obj.user >
"""

        target = XProtoTestHelpers.write_tmp_target("")
        args = FakeArgs()
        args.inputs = xproto
        args.target = target

        output = XOSGenerator.generate(args)

        self.assertTrue(True)

    def test_bin(self):
        xproto = \
"""
    policy slice_admin < slice.is_admin | obj.empty >
"""
        target = XProtoTestHelpers.write_tmp_target("")
        args = FakeArgs()
        args.inputs = xproto
        args.target = target

        output = XOSGenerator.generate(args)

        self.assertTrue(True)

        
    def test_exists(self):
        xproto = \
"""
    policy privilege < exists Privilege: Privilege.object_id = obj.id >
"""

        target = XProtoTestHelpers.write_tmp_target("")
        args = FakeArgs()
        args.inputs = xproto
        args.target = target

        output = XOSGenerator.generate(args)

        self.assertTrue(True)

    def test_forall(self):
        xproto = \
"""
    policy instance < forall Instance: exists Credential: Credential.obj_id = Instance.obj_id >
"""

        target = XProtoTestHelpers.write_tmp_target("")

        args = FakeArgs()
        args.inputs = xproto
        args.target = target

        output = XOSGenerator.generate(args)

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()


