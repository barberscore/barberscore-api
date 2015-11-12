# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0118_auto_20151111_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Built'), (20, b'Prepped'), (30, b'Flagged'), (35, b'Cleared'), (40, b'Confirmed'), (50, b'Final')]),
        ),
        migrations.AlterField(
            model_name='song',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Built'), (20, b'Prepped'), (30, b'Flagged'), (35, b'Cleared'), (40, b'Confirmed'), (50, b'Final')]),
        ),
    ]
