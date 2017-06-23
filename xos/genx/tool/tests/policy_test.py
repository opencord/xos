from xproto_test_base import *

class XProtoPolicyTests(XProtoTest):
    def test_constant(self):
        xproto = \
"""
    policy true_policy < true >
"""

        self.generate(xproto=xproto)
        self.assertTrue(True)

    def test_equal(self):
        xproto = \
"""
    policy slice_user < slice.user = obj.user >
"""

        self.generate(xproto=xproto)
        self.assertTrue(True)

    def test_bin(self):
        xproto = \
"""
    policy slice_admin < slice.is_admin | obj.empty >
"""

        self.generate(xproto=xproto)
        self.assertTrue(True)

    def test_exists(self):
        xproto = \
"""
    policy privilege < exists Privilege: Privilege.object_id = obj.id >
"""

        self.generate(xproto=xproto)
        self.assertTrue(True)

    def test_forall(self):
        xproto = \
"""
    policy instance < forall Instance: exists Credential: Credential.obj_id = Instance.obj_id >
"""

        self.generate(xproto=xproto)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()


