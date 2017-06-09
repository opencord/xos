#!/usr/bin/python

import argparse
from generator import *

parse = argparse.ArgumentParser(description='XOS Generative Toolchain')
parse.add_argument('--rev', dest='rev', action='store_true',default=False, help='Convert proto to xproto')
parse.add_argument('--target', dest='target', action='store',default=None, help='Output format, corresponding to <output>.yaml file', required=True)
parse.add_argument('--output', dest='output', action='store',default=None, help='Destination dir')
parse.add_argument('--attic', dest='attic', action='store',default=None, help='The location at which static files are stored')
parse.add_argument('--kvpairs', dest='kv', action='store',default=None, help='Key value pairs to make available to the target')
parse.add_argument('--write-to-file', dest='write_to_file', action='store',default=None, help='How to you want to save the output to file: single (one file for all), model (one file per model)')
parse.add_argument('--dest-file', dest='dest_file', action='store',default=None, help='The name of the file where to save the output (mandatory and used only if write-to-file is set to single)')
parse.add_argument('--dest-extension', dest='dest_extension', action='store',default=None, help='The extension of the file where to save the output (mandatory and used only if write-to-file is not single)')
parse.add_argument('files', metavar='<input file>', nargs='+', action='store', help='xproto files to compile')

class XosGen:

    @staticmethod
    def init(args=None):

        if not args:
            args = parse.parse_args()

        args.quiet = False

        # convert output to absolute path
        if args.output is not None and not os.path.isabs(args.output):
            args.output = os.path.abspath(os.getcwd() + '/' + args.output)
        if not os.path.isabs(args.target):
            args.target = os.path.abspath(os.getcwd() + '/' + args.target)

        inputs = []
        for fname in args.files:
            if not os.path.isabs(fname):
                inputs.append(os.path.abspath(os.getcwd() + '/' + fname))
            else:
                inputs.append(fname)
        args.files = inputs

        generated = XOSGenerator.generate(args)

        if not args.output and not args.write_to_file:
            print generated