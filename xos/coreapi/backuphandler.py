import os
import sys

from xosconfig import Config

# so django can find core.models
xos_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/..")
sys.path.append(xos_path)

from xosconfig import Config
from multistructlog import create_logger
log = create_logger(Config().get("logging"))

"""
apt-get update && \
apt-get install -y wget && \
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main" > /etc/apt/sources.list.d/PostgreSQL.list' && \
apt-get update && \
apt-get install -y postgresql-client-10
"""

"""
python standalone_backup_main.py && python backupprocessor.py
"""

class BackupHandler_django(object):
    """ This backuphandler uses django dumpdata and loaddata """
    def __init__(self):
        import django
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xos.settings")
        django.setup()
        from django.core.management import execute_from_command_line
        self.django_execute = execute_from_command_line

    def backup(self, filename):
        self.django_execute([sys.executable, "dumpdata", "-o", filename])

    def restore(self, filename):
        # TODO: clear database?
        self.django_execute([sys.executable, "loaddata", filename])


class BackupHandler_postgres(object):
    """ This backuphandler uses postgres pg_dump and xxx """
    def __init__(self):
        self.db_name = Config().get("database.name")
        self.db_username = Config().get("database.username")
        self.db_password = Config().get("database.password")
        self.db_host = "xos-db"
        self.db_port = "5432"

    def backup(self, filename):
        cmd = "PGPASSWORD=\"%s\" pg_dump -h %s -p %s -U %s -c %s > %s" % (self.db_password, self.db_host, self.db_port, self.db_username, self.db_name, filename)
        log.info("Shell execute: %s" % cmd)
        result = os.system(cmd)
        log.info("Shell result", result=result)
        if result != 0:
            raise Exception("pgdump failed")

    def restore(self, filename):
        cmd = "PGPASSWORD=\"%s\" psql -h %s -p %s -U %s %s < %s > /dev/null" % (self.db_password, self.db_host, self.db_port, self.db_username, self.db_name, filename)
        log.info("Shell execute: %s" % cmd)
        result = os.system(cmd)
        log.info("Shell result", result=result)
        if result != 0:
            raise Exception("psql failed")        


BackupHandler = BackupHandler_postgres
