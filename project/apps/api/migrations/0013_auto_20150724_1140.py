# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_catalog_bhs_songname'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalog',
            name='is_medley',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='catalog',
            name='is_parody',
            field=models.BooleanField(default=False),
        ),
    ]
