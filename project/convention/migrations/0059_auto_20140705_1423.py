# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def normplace(apps, schema_editor):
    Contestant = apps.get_model("convention", "Contestant")
    for contestant in Contestant.objects.exclude(place=None):
        contestant.normplace = contestant.place * 10
        contestant.save()


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0058_contestant_normplace'),
    ]

    operations = [
        migrations.RunPython(normplace)
    ]
