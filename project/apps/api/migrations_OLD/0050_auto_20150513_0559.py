# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0049_auto_20150512_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='session',
            field=models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2)]),
        ),
    ]
