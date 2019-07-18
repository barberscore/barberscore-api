# Generated by Django 2.2.3 on 2019-07-16 15:38

from django.db import migrations


def forward(apps, schema_editor):
    Convention = apps.get_model('cmanager.convention')
    User = apps.get_model('rest_framework_jwt.user')

    conventions = Convention.objects.all()

    for convention in conventions:
        pks = [
            'a88991ba-20f0-4948-a713-811d8b5dcd8a',
            '88b20557-f13e-42e4-8037-ac930d9e6362',
            '8b916eae-e3dd-4bdf-9a39-85773b97f421',
        ]
        us = User.objects.filter(
            id__in=pks,
        )
        for u in us:
            convention.owners.add(u)


class Migration(migrations.Migration):

    dependencies = [
        ('cmanager', '0014_convention_owners'),
    ]

    operations = [
        migrations.RunPython(forward),
    ]