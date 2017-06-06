#!/usr/bin/python

import pdb
import argparse
import traceback
import sys
import os
from generator import *

parse = argparse.ArgumentParser(description='XOS Generative Toolchain')
parse.add_argument('--rev', dest='rev', action='store_true',default=False, help='Convert proto to xproto')
parse.add_argument('--target', dest='target', action='store',default=None, help='Output format, corresponding to <output>.yaml file', required=True)
parse.add_argument('--output', dest='output', action='store',default=None, help='Destination dir', required=True)
parse.add_argument('--attic', dest='attic', action='store',default=None, help='The location at which static files are stored')
parse.add_argument('--kvpairs', dest='kv', action='store',default=None, help='Key value pairs to make available to the target')
parse.add_argument('inputs', metavar='<input file>', nargs='+', action='store', help='xproto files to compile')

args = parse.parse_args()

class XosGen:

    @staticmethod
    def init():

        args.quiet = False

        # convert output to absolute path
        if not os.path.isabs(args.output):
            args.output = os.path.abspath(os.getcwd() + '/' + args.output)
        if not os.path.isabs(args.target):
            args.target = os.path.abspath(os.getcwd() + '/' + args.target)

        inputs = []
        for fname in args.inputs:
            if not os.path.isabs(args.target):
                inputs.append(os.path.abspath(os.getcwd() + '/' + fname))
            else:
                inputs.append(fname)
        args.inputs = inputs

        generator = XOSGenerator(args)
        generator.generate()
