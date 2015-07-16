# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0146_auto_20150714_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='status',
            field=model_utils.fields.StatusField(default=b'Upcoming', max_length=100, verbose_name='status', no_check_for_status=True, choices=[(0, 'dummy')]),
        ),
        migrations.AddField(
            model_name='contest',
            name='status_changed',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status'),
        ),
    ]
