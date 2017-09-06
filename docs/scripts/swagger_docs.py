import os
from xosgenx.generator import XOSGenerator

CWD = OUTPUT_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
SWAGGER_DOCS_DIR = os.path.abspath(CWD + '/../swagger/specs')
ORCHESTRATION_DIR = os.path.abspath(CWD + "/../../../")
SERVICE_DIR = os.path.abspath(ORCHESTRATION_DIR + "/xos_services")

XOS_XPROTO = os.path.abspath(CWD + "/../../xos/core/models/core.xproto")

class Args:
    pass

def generate_swagger_docs(service, xproto):

    if not os.path.isfile(xproto):
        print "ERROR: Couldn't find xproto file for %s at: %s" % (service, xproto)
        return

    print "Generating swagger docs for %s [%s]" % (service, xproto)
    args = Args()
    args.inputs = open(xproto).read()
    args.target = 'swagger.xtarget'
    args.output = SWAGGER_DOCS_DIR
    args.write_to_file = "single"
    args.dest_file = "%s.yaml" % service
    args.quiet = False
    try:
        XOSGenerator.generate(args)
    except Exception, e:
        print "ERROR: Couldn't generate swagger specs for: %s" % service
        print e

def main():

    generate_swagger_docs('core', XOS_XPROTO)

    services = os.listdir(SERVICE_DIR)
    for service in services:
        xos_folder = os.path.abspath(SERVICE_DIR + "/%s/xos" % service);
        if os.path.isdir(xos_folder):
            for file in os.listdir(xos_folder):
                if 'xproto' in file:
                    generate_swagger_docs(service, os.path.abspath(xos_folder + "/%s" % file))
                else:
                    "WARNING: %s does not have an xproto file" % service
        else:
            print "WARNING: %s does not have an XOS folder" % service


if __name__ == '__main__':
    main()