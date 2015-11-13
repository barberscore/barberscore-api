# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0119_auto_20151111_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Built'), (15, b'Ready'), (20, b'Started'), (25, b'Finished'), (30, b'Final')]),
        ),
        migrations.AlterField(
            model_name='performance',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (20, b'Started'), (25, b'Finished'), (40, b'Confirmed'), (50, b'Final')]),
        ),
        migrations.AlterField(
            model_name='score',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (20, b'Entered'), (30, b'Flagged'), (35, b'Validated'), (40, b'Confirmed'), (50, b'Final')]),
        ),
        migrations.AlterField(
            model_name='session',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Built'), (15, b'Ready'), (20, b'Started'), (25, b'Finished'), (30, b'Final')]),
        ),
        migrations.AlterField(
            model_name='song',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (20, b'Entered'), (40, b'Confirmed'), (50, b'Final')]),
        ),
    ]
