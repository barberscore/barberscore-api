# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0051_auto_20150201_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='chorusperformance',
            name='place',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quartetperformance',
            name='place',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
