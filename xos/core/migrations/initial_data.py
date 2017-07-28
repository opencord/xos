import os
import yaml
from django.db import models, migrations
from datetime import date

FIXTURES = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/initial_data.yaml')

def load_data_from_yaml():
    file = open(FIXTURES, 'r').read()
    try:
        data = yaml.load(file)
        return data
    except Exception, e:
        raise Exception("Cannot load inital data file: %s" % e.message)


def persist_data(apps, schema_editor):

    data = load_data_from_yaml()

    # iterate over the data
    for entry in data:

        # retrieve the class for that model
        [app, model_name] = entry['model'].split('.')
        model_class = apps.get_model(app, model_name)

        # create a new instance for that model
        i = model_class(**entry['fields'])

        # check relations
        if 'relations' in entry:
            for (r_name, r) in entry['relations'].items():
                # retrieve the related model
                [r_app, r_model_name] = r['model'].split('.')
                related_model_class = apps.get_model(r_app, r_model_name)
                r_model = related_model_class.objects.get(**r['fields'])

                # assign relation
                setattr(i, r_name, r_model)

        # save the instance
        i.save()
        print "Created %s: %s" % (model_name, entry['fields'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(persist_data)
    ]