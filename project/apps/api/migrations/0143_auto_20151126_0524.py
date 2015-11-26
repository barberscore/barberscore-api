# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import django_fsm
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0142_auto_20151125_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New')]),
        ),
        migrations.AddField(
            model_name='award',
            name='status_monitor',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, help_text=b'Status last updated', monitor=b'status'),
        ),
    ]
