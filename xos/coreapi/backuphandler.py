import sys

# so django can find core.models
xos_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/..")
sys.path.append(xos_path)

class BackupHandler(object):
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