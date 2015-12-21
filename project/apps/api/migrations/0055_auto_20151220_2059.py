# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields.ranges


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0054_auto_20151220_2057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='start_time',
        ),
        migrations.AddField(
            model_name='organization',
            name='date',
            field=django.contrib.postgres.fields.ranges.DateRangeField(help_text=b'\n            The active dates of the resource.', null=True, blank=True),
        ),
    ]
