# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0109_auto_20151110_0729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Structured'), (12, b'Impaneled'), (15, b'Ready'), (20, b'Current'), (25, b'Review'), (30, b'Complete')]),
        ),
    ]
