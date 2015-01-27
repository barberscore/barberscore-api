# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import timezone_field.fields
import django_pg.models.fields.datetime_


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_auto_20150127_0820'),
    ]

    operations = [
        migrations.AddField(
            model_name='chorusperformance',
            name='stagetime',
            field=django_pg.models.fields.datetime_.DateTimeField(help_text=b'\n            The title of the first song of the performance.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contest',
            name='timezone',
            field=timezone_field.fields.TimeZoneField(default=b'US/Pacific'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quartetperformance',
            name='stagetime',
            field=django_pg.models.fields.datetime_.DateTimeField(help_text=b'\n            The title of the first song of the performance.', null=True, blank=True),
            preserve_default=True,
        ),
    ]
