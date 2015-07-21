# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='is_medley',
        ),
        migrations.RemoveField(
            model_name='song',
            name='is_parody',
        ),
        migrations.AddField(
            model_name='chart',
            name='is_medley',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='chart',
            name='is_parody',
            field=models.BooleanField(default=False),
        ),
    ]
