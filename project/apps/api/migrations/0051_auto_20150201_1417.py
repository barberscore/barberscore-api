# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0050_auto_20150201_1348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='district',
            name='abbreviation',
        ),
        migrations.AddField(
            model_name='district',
            name='long_name',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
