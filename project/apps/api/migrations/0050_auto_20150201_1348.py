# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def swap_district_name_step1(apps, schema_editor):
    d = apps.get_model('api', 'District')

    districts = d.objects.all()
    for district in districts:
        district.notes = district.name
        district.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0049_contest_scoresheet_csv'),
    ]

    operations = [
        migrations.RunPython(swap_district_name_step1)
    ]
