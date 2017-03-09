import sys
sys.path.append("..")

from xosapi import xos_grpc_client

def test_callback():
    print "TEST: vsg_introspect"

    c = xos_grpc_client.coreclient

    for vsg in c.xos_orm.VSGTenant.objects.all():
        print "  vsg", vsg.id
        for field_name in ["public_ip", "public_mac", "netbits", "gateway_ip", "gateway_mac", "wan_vm_ip", "wan_vm_mac"]:
            print "    %s: %s" % (field_name, getattr(vsg, field_name))

    print "    okay"

xos_grpc_client.start_api_parseargs(test_callback)

