# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20151203_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panel',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Built'), (20, b'Started'), (30, b'Final')]),
        ),
    ]
