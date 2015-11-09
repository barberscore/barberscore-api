# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0105_contest_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='state',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Structured'), (15, b'Ready'), (20, b'Current'), (25, b'Review'), (30, b'Complete')]),
        ),
    ]
