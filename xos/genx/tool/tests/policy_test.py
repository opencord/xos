from xproto_test_base import *

class XProtoPolicyTests(XProtoTest):
    def test_constant(self):
        xproto = \
"""
    policy < true >
"""

        self.generate(target=target)
        self.assertTrue(True)

    def test_equal(self):
        xproto = \
"""
    policy < slice.user = obj.user >
"""

        self.generate(target=target)
        self.assertTrue(True)

    def test_bin(self):
        xproto = \
"""
    policy < slice.is_admin | obj.empty >
"""

        self.generate(target=target)
        self.assertTrue(True)

    def test_exists(self):
        xproto = \
"""
    policy < exists Privilege: Privilege.object_id = obj.id >
"""

        self.generate(target=target)
        self.assertTrue(True)

    def test_forall(self):
        xproto = \
"""
    policy < forall Instance: instance.slice = obj exists Credential: Credential.obj_id = Instance.obj_id >
"""

        self.generate(target=target)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()


