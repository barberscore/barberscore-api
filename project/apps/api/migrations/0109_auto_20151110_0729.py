# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0108_auto_20151110_0723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Ready'), (20, b'Current'), (30, b'Complete')]),
        ),
        migrations.AlterField(
            model_name='performance',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Structured'), (15, b'Ready'), (20, b'Current'), (25, b'Review'), (30, b'Complete')]),
        ),
        migrations.AlterField(
            model_name='score',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Flagged'), (20, b'Passed'), (30, b'Complete')]),
        ),
        migrations.AlterField(
            model_name='session',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Structured'), (15, b'Ready'), (20, b'Current'), (25, b'Review'), (30, b'Complete')]),
        ),
        migrations.AlterField(
            model_name='song',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Flagged'), (20, b'Passed'), (30, b'Complete')]),
        ),
    ]
