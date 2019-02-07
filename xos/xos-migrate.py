# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/python

# TO RUN
# source scripts/setup_venv.sh
# pip install django django_extensions psycopg2 djangorestframework
# python xos-migrate.py [-s <service-name>]
# eg: python xos-migrate.py -s core -s fabric

# TODO
# - add support for services that are in the cord/orchestration/profiles folders
# - add support to specify a name to be given to the generated migration (--name parameter in django makemigrations)

import os
import argparse
import yaml
import shutil
import logging
from logging import Formatter
from copy import copy
from xosgenx.generator import XOSProcessor, XOSProcessorArgs


# LOGGING - Move to antoher file
class ColoredFormatter(Formatter):
    MAPPING = {
        'DEBUG': 37,  # white
        'INFO': 36,  # cyan
        'WARNING': 33,  # yellow
        'ERROR': 31,  # red
        'CRITICAL': 41,  # white on red bg
    }

    PREFIX = '\033['
    SUFFIX = '\033[0m'

    def __init__(self, patern):
        Formatter.__init__(self, patern)

    def format(self, record):
        colored_record = copy(record)

        levelname = colored_record.levelname
        message = colored_record.msg

        seq = self.MAPPING.get(levelname, 37) # default white

        colored_levelname = ('{0}{1}m{2}{3}') \
            .format(self.PREFIX, seq, levelname, self.SUFFIX)
        colored_message = ('{0}{1}m{2}{3}') \
            .format(self.PREFIX, seq, message, self.SUFFIX)

        colored_record.levelname = colored_levelname
        colored_record.msg = colored_message
        return Formatter.format(self, colored_record)

log = logging.getLogger("xos-migrate")

def get_abs_path(path):
    if os.path.isabs(path):
        return path
    return os.path.dirname(os.path.realpath(__file__)) + "/" + path

# CONSTANTS

SERVICE_BASE_DIR = get_abs_path("../../xos_services/")
SERVICE_DEST_DIR = get_abs_path("services")

# TODO make configurable
CORE_MODELS_DIR = get_abs_path("core/models/")
CORE_MODELS_XPROTO = os.path.join(CORE_MODELS_DIR, "core.xproto")


def print_banner():
    log.info(r"---------------------------------------------------------------")
    log.info(r"                                    _                  __      ")
    log.info(r"   _  ______  _____      ____ ___  (_)___ __________ _/ /____  ")
    log.info(r"  | |/_/ __ \/ ___/_____/ __ `__ \/ / __ `/ ___/ __ `/ __/ _ \ ")
    log.info(r" _>  </ /_/ (__  )_____/ / / / / / / /_/ / /  / /_/ / /_/  __/ ")
    log.info(r"/_/|_|\____/____/     /_/ /_/ /_/_/\__, /_/   \__,_/\__/\___/  ")
    log.info(r"                                  /____/                       ")
    log.info(r"---------------------------------------------------------------")
    log.debug("Storing logs in: %s" % os.environ["LOG_FILE"])
    log.debug("Config schema: %s" % os.environ['XOS_CONFIG_SCHEMA'])
    log.debug("Config: %s" % os.environ['XOS_CONFIG_FILE'])
    log.debug(r"---------------------------------------------------------------")


def config_logger(verbose):
    if verbose:
        log.setLevel(level=logging.DEBUG)
    else:
        log.setLevel(level=logging.INFO)

    # Add console handler using our custom ColoredFormatter
    ch = logging.StreamHandler()
    if verbose:
        ch.setLevel(level=logging.DEBUG)
    else:
        ch.setLevel(level=logging.INFO)
    cf = ColoredFormatter("[%(name)s] [%(levelname)s]  %(message)s (%(filename)s:%(lineno)d)")
    ch.setFormatter(cf)
    log.addHandler(ch)



def generate_core_models():
    args = XOSProcessorArgs(
        output=CORE_MODELS_DIR,
        target= "django.xtarget",
        dest_extension= "py",
        write_to_file= "model",
        files=[CORE_MODELS_XPROTO],
    )
    XOSProcessor.process(args)

    security_args = XOSProcessorArgs(
        output=CORE_MODELS_DIR,
        target="django-security.xtarget",
        dest_file="security.py",
        write_to_file="single",
        files=[CORE_MODELS_XPROTO],
    )

    XOSProcessor.process(security_args)

    init_args = XOSProcessorArgs(
        output = CORE_MODELS_DIR,
        target = "init.xtarget",
        dest_file = "__init__.py",
        write_to_file = "single",
        files = [CORE_MODELS_XPROTO],
    )
    XOSProcessor.process(init_args)


def find_xproto_in_folder(path):
    """
    Recursively iterate a folder tree to look for any xProto file.
    We use this function in case that the name of the xProto is different from the name of the folder (eg: olt-service)
    :param path: the root folder to start the search
    :return: [string]
    """
    xprotos = []
    for fn in os.listdir(path):
        # skip hidden files and folders. plus other useless things
        if fn.startswith(".") or fn == "venv-xos" or fn == "htmlcov":
            continue
        full_path = os.path.join(path, fn)
        if fn.endswith(".xproto"):
            xprotos.append(full_path)
        elif os.path.isdir(full_path):
            xprotos = xprotos + find_xproto_in_folder(full_path)
    return xprotos


def find_decls_models(path):
    """
    Recursively iterate a folder tree to look for any models.py file.
    This files contain the base model for _decl generated models.
    :param path: the root folder to start the search
    :return: [string]
    """
    decls = []
    for fn in os.listdir(path):
        # skip hidden files and folders. plus other useless things
        if fn.startswith(".") or fn == "venv-xos" or fn == "htmlcov":
            continue
        full_path = os.path.join(path, fn)
        if fn == "models.py":
            decls.append(full_path)
        elif os.path.isdir(full_path):
            decls = decls + find_decls_models(full_path)
    return decls


def get_service_name_from_config(path):
    """
    Given a service folder look for the config.yaml file and find the name
    :param path: the root folder to start the search
    :return: string
    """
    config = os.path.join(path, "xos/synchronizer/config.yaml")
    if not os.path.isfile(config):
        raise Exception("Config file not found at: %s" % config)

    cfg_file = open(config)
    cfg = yaml.load(cfg_file)
    return cfg['name']


def generate_service_models(service_dir, service_name):
    """
    Generate the django code starting from xProto for a given service.
    :param service_dir: string (path to the folder)
    :param service_name: string (name of the service)
    :return: void
    """
    xprotos = find_xproto_in_folder(service_dir)
    decls = find_decls_models(service_dir)
    log.debug("Generating models for %s from files %s" % (service_name, ", ".join(xprotos)))
    out_dir = os.path.join(SERVICE_DEST_DIR, service_name)
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    args = XOSProcessorArgs(
        output=out_dir,
        files=xprotos,
        target = "service.xtarget",
        write_to_file = "target",
    )
    XOSProcessor.process(args)

    security_args = XOSProcessorArgs(
        output=out_dir,
        target="django-security.xtarget",
        dest_file="security.py",
        write_to_file="single",
        files=xprotos,
    )

    XOSProcessor.process(security_args)

    init_py_filename = os.path.join(out_dir, "__init__.py")
    if not os.path.exists(init_py_filename):
        open(init_py_filename, "w").write("# created by dynamicbuild")

    # copy over models.py files from the service
    if len(decls) > 0:
        for file in decls:
            fn = os.path.basename(file)
            src_fn = file
            dest_fn = os.path.join(out_dir, fn)
            log.debug("Copying models.py from %s to %s" % (src_fn, dest_fn))
            shutil.copyfile(src_fn, dest_fn)

    # copy existing migrations from the service, otherwise they won't be incremental
    src_dir = os.path.join(service_dir, "xos", "synchronizer", "migrations")
    if os.path.isdir(src_dir):
        dest_dir = os.path.join(out_dir, "migrations")
        if os.path.isdir(dest_dir):
            shutil.rmtree(dest_dir)  # empty the folder, we'll copy everything again
        shutil.copytree(src_dir, dest_dir)


def copy_service_migrations(service_dir, service_name):
    """
    Once the migrations are generated, copy them in the correct location
    :param service_dir: string (path to the folder)
    :param service_name: string (name of the service)
    :return: void
    """
    # FIXME Django eats this message
    log.debug("Copying %s migrations to %s" % (service_name, service_dir))
    migration_dir = os.path.join(SERVICE_DEST_DIR, service_name, "migrations")
    dest_dir = os.path.join(service_dir, "xos", "synchronizer", "migrations")
    if os.path.isdir(dest_dir):
        shutil.rmtree(dest_dir)  # empty the folder, we'll copy everything again
    shutil.copytree(migration_dir, dest_dir)

# SETTING ENV
os.environ['LOG_FILE'] = get_abs_path("django.log")
os.environ['XOS_CONFIG_SCHEMA'] = get_abs_path("migration_cfg_schema.yaml")
os.environ['XOS_CONFIG_FILE'] = get_abs_path("migration_cfg.yaml")
os.environ["MIGRATIONS"] = "true"
os.environ["INSTALLED_APPS"] = "" # this is populated in case we generate migrations for services and it's used in settings.py

# PARAMS
parser = argparse.ArgumentParser(description="XOS Migrations")

parser.add_argument(
    '-s',
    '--service',
    action='append',
    dest="service_names",
    help='The name of the folder containing the service in cord/orchestration/xos_services'
)

parser.add_argument(
    "-v",
    "--verbose",
    help="increase output verbosity",
    action="store_true"
)

if __name__ == "__main__":
    args = parser.parse_args()

    config_logger(args.verbose)

    print_banner()

    log.info("Services: %s" % ", ".join(args.service_names))

    django_cli_args = ['xos-migrate.py', 'makemigrations']

    # generate the code for each service and create a list of parameters to pass to django
    app_list = []
    for service in args.service_names:
        if service == "core":
            generate_core_models()
            django_cli_args.append("core")
        else:
            service_dir = os.path.join(SERVICE_BASE_DIR, service)
            service_name = get_service_name_from_config(service_dir)
            generate_service_models(service_dir, service_name)
            app_list.append("services.%s" % service_name)

            django_cli_args.append(service_name)

    os.environ["INSTALLED_APPS"] = ",".join(app_list)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xos.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(django_cli_args)

    # copying migrations back to the service
    for service in args.service_names:
        if service == "core":
            # we don't need to copy migrations for the core
            continue
        else:
            service_dir = os.path.join(SERVICE_BASE_DIR, service)
            service_name = get_service_name_from_config(service_dir)
            copy_service_migrations(service_dir, service_name)
