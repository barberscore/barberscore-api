# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields.ranges


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0122_auto_20160213_0830'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='qual',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='award',
            name='size',
            field=django.contrib.postgres.fields.ranges.IntegerRangeField(null=True, blank=True),
        ),
    ]
