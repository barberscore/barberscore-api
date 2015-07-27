# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20150726_2248'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='is_parody',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='spot',
            name='name',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
