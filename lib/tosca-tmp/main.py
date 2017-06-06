import os
import sys

# HACK directory for the gen tools
gen_tools_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../../xos/genx/tool/")
sys.path.append(gen_tools_dir)

XPROTO_FILE = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/myproto.xproto")
XTARGET_FILE = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/tosca.xtarget")
OUTPUT_FILE = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/out")

from generator import XOSGenerator

# Defining ARGS
class Args:
    def __init__(self):
        self.inputs = [XPROTO_FILE]
        self.input = open(XPROTO_FILE).read()
        self.rev = False # what's rev used for??
        self.target = XTARGET_FILE
        self.output = OUTPUT_FILE
        self.kv = 'foo:bar'

TOSCA_ARGS = Args()

class TOSCAGenerator:
    def __init__(self):
        genx = XOSGenerator(TOSCA_ARGS)
        genx.input = TOSCA_ARGS.input # why do I have to manually add this??
        tosca = genx.generate()
        print tosca


if __name__ == '__main__':
    TOSCAGenerator()