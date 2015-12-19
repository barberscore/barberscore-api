# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields.ranges


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0049_auto_20151218_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='dates',
            field=django.contrib.postgres.fields.ranges.DateRangeField(help_text=b'\n            The active dates of the resource.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='convention',
            name='dates2',
            field=django.contrib.postgres.fields.ranges.DateRangeField(help_text=b'\n            The convention dates (will be replaced by start/end).', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='group',
            name='dates',
            field=django.contrib.postgres.fields.ranges.DateRangeField(help_text=b'\n            The active dates of the resource.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='actual',
            field=django.contrib.postgres.fields.ranges.DateTimeRangeField(help_text=b'\n            The actual performance window.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='scheduled',
            field=django.contrib.postgres.fields.ranges.DateTimeRangeField(help_text=b'\n            The scheduled performance window.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='dates',
            field=django.contrib.postgres.fields.ranges.DateRangeField(help_text=b'\n            The active dates of the resource.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='round',
            name='dates',
            field=django.contrib.postgres.fields.ranges.DateRangeField(help_text=b'\n            The active dates of the resource.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='session',
            name='dates',
            field=django.contrib.postgres.fields.ranges.DateRangeField(help_text=b'\n            The active dates of the session.', null=True, blank=True),
        ),
    ]
