# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import django_fsm
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_auto_20151209_1801'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapter',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='group',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='person',
            name='is_active',
        ),
        migrations.AddField(
            model_name='chapter',
            name='sts',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Active'), (20, b'Inactive')]),
        ),
        migrations.AddField(
            model_name='chapter',
            name='sts_monitor',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, help_text=b'Status last updated', monitor=b'sts'),
        ),
        migrations.AddField(
            model_name='group',
            name='sts',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Active'), (20, b'Inactive')]),
        ),
        migrations.AddField(
            model_name='group',
            name='sts_monitor',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, help_text=b'Status last updated', monitor=b'sts'),
        ),
        migrations.AddField(
            model_name='organization',
            name='lvl',
            field=models.IntegerField(blank=True, help_text=b'\n            The level of the contest.  Note that this may be different than the level of the parent session.', null=True, choices=[(1, b'International'), (2, b'District'), (3, b'Division')]),
        ),
        migrations.AddField(
            model_name='organization',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Active'), (20, b'Inactive')]),
        ),
        migrations.AddField(
            model_name='organization',
            name='status_monitor',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, help_text=b'Status last updated', monitor=b'status'),
        ),
        migrations.AddField(
            model_name='person',
            name='sts',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Active'), (20, b'Inactive')]),
        ),
        migrations.AddField(
            model_name='person',
            name='sts_monitor',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, help_text=b'Status last updated', monitor=b'sts'),
        ),
    ]
