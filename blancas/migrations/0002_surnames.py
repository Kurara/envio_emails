# Generated by Django 2.2 on 2020-08-31 20:35

from django.db import migrations, models
from blancas.surnames import surnames


class Migration(migrations.Migration):

    initial = True

    dependencies = [('blancas', '0001_initial')]

    def insert_surnames(apps, schema_editor):
        Surnames = apps.get_model("blancas", "Surname")
        for item in surnames:
            Surnames.objects.bulk_create(
                [Surnames(surname=item)]
            )

    def reverse_func(apps, schema_editor):
        # forwards_func() creates two Country instances,
        # so reverse_func() should delete them.
        Surnames = apps.get_model("blancas", "Surname")
        

    operations = [
        migrations.RunPython(insert_surnames, reverse_func)
    ]
