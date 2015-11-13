# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0121_auto_20151112_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Built'), (20, b'Started'), (25, b'Finished'), (30, b'Final')]),
        ),
        migrations.AlterField(
            model_name='song',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (40, b'Confirmed'), (50, b'Final')]),
        ),
    ]
