#!/usr/bin/env python

import os
from xosgenx.generator import XOSProcessor, XOSProcessorArgs

# These assume a traditional CORD/SEBA hierarchy is checked out using `repo`

SCRIPT_DIR=os.path.dirname(os.path.realpath(__file__))
BASE_DIR=os.path.join(SCRIPT_DIR,"..","..","..")
SERVICES_DIR=os.path.join(BASE_DIR,"orchestration","xos_services")
CORE_XPROTO=os.path.join(BASE_DIR,"orchestration","xos","xos","core","models","core.xproto")
TARGET=os.path.join(BASE_DIR,"orchestration","xos","lib","xos-genx","xosgenx","targets","fieldlist.xtarget")

def get_all_xproto():
    xprotos=[]
    for service_name in os.listdir(SERVICES_DIR):
        if service_name.startswith("."):
            continue
        service_path = os.path.join(SERVICES_DIR, service_name)
        if not os.path.isdir(service_path):
            continue
        models_dir = os.path.join(service_path, "xos", "synchronizer", "models")
        if not os.path.isdir(models_dir):
            continue
        for xproto_name in os.listdir(models_dir):
            if xproto_name.startswith("."):
                continue
            if not xproto_name.endswith(".xproto"):
                continue
            xproto_pathname = os.path.join(models_dir, xproto_name)
            xprotos.append(xproto_pathname)
    return xprotos

xprotos = get_all_xproto() + [CORE_XPROTO]
args = XOSProcessorArgs(files=xprotos,
                        target=TARGET,
                        verbosity=1
                        )
output = XOSProcessor.process(args)
