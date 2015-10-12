# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20151012_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='dates',
            field=models.CharField(help_text=b'\n            The convention dates (will be replaced by start/end).', max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='convention',
            name='is_active',
            field=models.BooleanField(default=True, help_text=b'\n            A boolean flag to indicate this convention should be included in results.'),
        ),
        migrations.AlterField(
            model_name='convention',
            name='kind',
            field=models.IntegerField(blank=True, help_text=b'\n            The kind of convention.', null=True, choices=[(1, b'International'), (2, b'Midwinter'), (3, b'Fall'), (4, b'Spring'), (5, b'Pacific')]),
        ),
        migrations.AlterField(
            model_name='convention',
            name='location',
            field=models.CharField(help_text=b'\n            The location of the convention ', max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='convention',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the convention (determined programmatically.)', unique=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='convention',
            name='timezone',
            field=timezone_field.fields.TimeZoneField(default=b'US/Pacific', help_text=b'\n            The local timezone of the convention '),
        ),
        migrations.AlterField(
            model_name='district',
            name='is_active',
            field=models.BooleanField(default=True, help_text=b'\n            A boolean for active/living resources.'),
        ),
        migrations.AlterField(
            model_name='group',
            name='is_active',
            field=models.BooleanField(default=True, help_text=b'\n            A boolean for active/living resources.'),
        ),
        migrations.AlterField(
            model_name='person',
            name='is_active',
            field=models.BooleanField(default=True, help_text=b'\n            A boolean for active/living resources.'),
        ),
    ]
