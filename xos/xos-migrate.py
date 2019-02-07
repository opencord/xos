# TO RUN
# source scripts/setup_venv.sh
# pip install django django_extensions psycopg2 djangorestframework
# python xos-migrate.py makemigrations core

import os
import sys
from xosgenx.generator import XOSProcessor, XOSProcessorArgs

def get_abs_path(path):
    if os.path.isabs(path):
        return path
    return os.path.dirname(os.path.realpath(__file__)) + "/" + path

def print_banner():
    print r"---------------------------------------------------------------"
    print r"                                    _                  __      "
    print r"   _  ______  _____      ____ ___  (_)___ __________ _/ /____  "
    print r"  | |/_/ __ \/ ___/_____/ __ `__ \/ / __ `/ ___/ __ `/ __/ _ \ "
    print r" _>  </ /_/ (__  )_____/ / / / / / / /_/ / /  / /_/ / /_/  __/ "
    print r"/_/|_|\____/____/     /_/ /_/ /_/_/\__, /_/   \__,_/\__/\___/  "
    print r"                                  /____/                       "
    print r"---------------------------------------------------------------"
    print "Storing logs in: %s" % os.environ["LOG_FILE"]
    print "Config schema: %s" % os.environ['XOS_CONFIG_SCHEMA']
    print "Config: %s" % os.environ['XOS_CONFIG_FILE']
    print r"---------------------------------------------------------------"

# CONSTANTS
# TODO make configurable
CORE_MODELS_DIR = get_abs_path("core/models/")
CORE_MODELS_XPROTO = os.path.join(CORE_MODELS_DIR, "core.xproto")

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

# SETTING ENV
os.environ['LOG_FILE'] = get_abs_path("django.log")
os.environ['XOS_CONFIG_SCHEMA'] = get_abs_path("migration_cfg_schema.yaml")
os.environ['XOS_CONFIG_FILE'] = get_abs_path("migration_cfg.yaml")
os.environ["MIGRATIONS"] = "true"

if __name__ == "__main__":
    print_banner()

    generate_core_models()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xos.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

