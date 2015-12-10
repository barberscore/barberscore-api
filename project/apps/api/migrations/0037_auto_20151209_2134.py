# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import django_fsm
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_auto_20151209_2110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='lvl',
        ),
        migrations.AddField(
            model_name='chapter',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Active'), (20, b'Inactive')]),
        ),
        migrations.AddField(
            model_name='chapter',
            name='status_monitor',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, help_text=b'Status last updated', monitor=b'status'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='level',
            field=models.IntegerField(blank=True, help_text=b'\n            The level of the contest.  Note that this may be different than the level of the parent session.', null=True, choices=[(0, b'International'), (1, b'District'), (2, b'Division')]),
        ),
    ]
