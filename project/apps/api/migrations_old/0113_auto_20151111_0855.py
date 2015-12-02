# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0112_auto_20151110_1440'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='start',
        ),
        migrations.RemoveField(
            model_name='session',
            name='start',
        ),
        migrations.AlterField(
            model_name='contest',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Built'), (15, b'Prepped'), (20, b'Started'), (25, b'Finished'), (30, b'Final')]),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Qualified'), (20, b'Accepted'), (30, b'Declined'), (40, b'Dropped'), (50, b'Competing'), (60, b'Finished'), (90, b'Final')]),
        ),
        migrations.AlterField(
            model_name='convention',
            name='status',
            field=models.IntegerField(default=0, help_text=b'The current status', choices=[(0, b'New'), (10, b'Built'), (20, b'Started'), (30, b'Final')]),
        ),
        migrations.AlterField(
            model_name='panelist',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (10, b'Scheduled'), (20, b'Confirmed'), (30, b'Final')]),
        ),
        migrations.AlterField(
            model_name='performance',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Built'), (15, b'Prepped'), (20, b'Started'), (25, b'Finished'), (30, b'Final')]),
        ),
        migrations.AlterField(
            model_name='score',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (5, b'Prepped'), (10, b'Flagged'), (20, b'Passed'), (30, b'Final')]),
        ),
        migrations.AlterField(
            model_name='session',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Built'), (15, b'Prepped'), (20, b'Started'), (25, b'Finished'), (30, b'Final')]),
        ),
        migrations.AlterField(
            model_name='song',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (20, b'Built'), (20, b'Prepped'), (30, b'Flagged'), (40, b'Passed'), (50, b'Final')]),
        ),
    ]
