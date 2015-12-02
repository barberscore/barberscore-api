# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0111_auto_20151110_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Qualified'), (20, b'Accepted'), (30, b'Declined'), (40, b'Dropped'), (50, b'Competing'), (60, b'Finished'), (90, b'Complete')]),
        ),
    ]
