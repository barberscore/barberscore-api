# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20150208_0950'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='groupfinish',
            options={'ordering': ('seed',)},
        ),
        migrations.AddField(
            model_name='performance',
            name='session',
            field=models.IntegerField(default=1, null=True, blank=True, choices=[(1, 1), (2, 2)]),
        ),
    ]
