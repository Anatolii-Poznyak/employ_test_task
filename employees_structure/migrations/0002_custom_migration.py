from django.core.management import call_command
from django.db import migrations


def create_json_with_data(apps, schema_editor):
    call_command("db_seeder", 1000, 3)


def create_superuser(apps, schema_editor):
    call_command("create_superuser")


def load_to_db(apps, schema_editor):
    json_file = "/app/employee_data.json"
    call_command("loaddata", json_file)


class Migration(migrations.Migration):

    dependencies = [
        ("employees_structure", "0001_initial"),
    ]

    """If we want to work with this code in future - we need to add argument elidable=True to this custom migrations,
     so they will be look like: 
     'migrations.RunPython(create_json_with_data, reverse_code=migrations.RunPython.noop, elidable=True'
     so it will be not applied in future, after it was applied at least once. At we will be able to make changes
     in models, change structure of DB, and superuser + json fake data will not been recreated/reloaded every time"""

    operations = [
        migrations.RunPython(create_json_with_data),
        migrations.RunPython(create_superuser),
        migrations.RunPython(load_to_db),
    ]

