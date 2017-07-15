import unittest
from xosgenx.generator import XOSGenerator
from helpers import FakeArgs, XProtoTestHelpers
import pdb

"""
The tests below use the Python code target to generate 
Python security policies, set up an appropriate environment and execute the Python.
"""
class XProtoSecurityTest(unittest.TestCase):
    def setUp(self):
        self.target = XProtoTestHelpers.write_tmp_target("{{ xproto_fol_to_python_test(proto.policies.test_policy, None, '0') }}")

    def test_constant(self):
        xproto = \
"""
    policy test_policy < True >
"""
        args = FakeArgs()
        args.inputs = xproto
        args.target = self.target

        output = XOSGenerator.generate(args)

        exec(output) # This loads the generated function, which should look like this:

        """
        def policy_output_0(obj, ctx):
            i1 = True
            return i1
        """

        verdict = policy_output_0({}, {})
        self.assertTrue(verdict)

    def test_equal(self):
        xproto = \
"""
    policy test_policy < ctx.user = obj.user >
"""

        args = FakeArgs()
        args.inputs = xproto
        args.target = self.target

        output = XOSGenerator.generate(args)

        exec(output) # This loads the generated function, which should look like this:

        """
        def policy_output_0(obj, ctx):
            i1 = (ctx.user == obj.user)
            return i1
        """

        obj = FakeArgs()
	obj.user = 1
        ctx = FakeArgs()
	ctx.user = 1

        verdict = policy_output_0(obj, ctx)

    def test_bin(self):
        xproto = \
"""
    policy test_policy < ctx.is_admin = True | obj.empty = True>
"""

        args = FakeArgs()
        args.inputs = xproto
        args.target = self.target

        output = XOSGenerator.generate(args)
        exec(output) # This loads the generated function, which should look like this:

        """
	def policy_output_0(obj, ctx):
	    i2 = (ctx.is_admin == True)
	    i3 = (obj.empty == True)
	    i1 = (i2 or i3)
	    return i1
        """

        obj = FakeArgs()
	obj.empty = True

	ctx = FakeArgs()
	ctx.is_admin = True

        verdict = policy_output_0(obj, ctx)

        self.assertTrue(verdict)

        
    def test_exists(self):
        xproto = \
"""
    policy test_policy < exists Privilege: Privilege.object_id = obj.id >
"""
	args = FakeArgs()
        args.inputs = xproto
        args.target = self.target

        output = XOSGenerator.generate(args)
        exec(output) # This loads the generated function, which should look like this:

        """
	def policy_output_0(obj, ctx):
	    i1 = Privilege.objects.filter(object_id=obj.id)
    	    return i1
        """

        self.assertTrue(policy_output_0 is not None)
	
    def _test_python(self):
        xproto = \
"""
    policy test_policy < {{ (5 > 2) }} = True >
"""
	args = FakeArgs()
        args.inputs = xproto
        args.target = self.target
        output = XOSGenerator.generate(args)
        exec(output) # This loads the generated function, which should look like this:
	print output

        """
	def policy_output_0(obj, ctx):
	    i1 = Privilege.objects.filter(object_id=obj.id)
	    return i1
        """

        self.assertTrue(policy_output_0 is not None)

    def test_forall(self):
        # This one we only parse
        xproto = \
"""
    policy test_policy < forall Instance: exists Credential: Credential.obj_id = Instance.obj_id >
"""

        target = XProtoTestHelpers.write_tmp_target("{{ proto.policies.instance }}")

        args = FakeArgs()
        args.inputs = xproto
        args.target = target

        output = XOSGenerator.generate(args)
        (op, operands), = eval(output).items()

        self.assertEqual(op,'forall')


if __name__ == '__main__':
    unittest.main()


