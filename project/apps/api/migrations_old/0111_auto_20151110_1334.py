# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0110_auto_20151110_0844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Structured'), (15, b'Ready'), (20, b'Started'), (25, b'Finished'), (30, b'Complete')]),
        ),
    ]
