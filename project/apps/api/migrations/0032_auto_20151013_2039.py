# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_auto_20151013_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='district',
            field=models.ForeignKey(related_name='contests', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.District', null=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='level',
            field=models.IntegerField(default=1, choices=[(1, b'International')]),
        ),
        migrations.AlterField(
            model_name='convention',
            name='location',
            field=models.CharField(help_text=b'\n            The location of the convention.', max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='convention',
            name='timezone',
            field=timezone_field.fields.TimeZoneField(default=b'US/Pacific', help_text=b'\n            The local timezone of the convention.'),
        ),
    ]
