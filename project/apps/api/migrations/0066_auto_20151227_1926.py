# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0065_auto_20151227_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Built'), (20, b'Started'), (20, b'Finished'), (50, b'Final')]),
        ),
    ]
