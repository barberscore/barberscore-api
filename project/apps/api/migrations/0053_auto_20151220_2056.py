# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields.ranges


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0052_auto_20151220_2036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='award',
            name='is_championship',
        ),
        migrations.RemoveField(
            model_name='convention',
            name='dates',
        ),
        migrations.AddField(
            model_name='certification',
            name='date',
            field=django.contrib.postgres.fields.ranges.DateRangeField(help_text=b'\n            The active dates of the resource.', null=True, blank=True),
        ),
    ]
