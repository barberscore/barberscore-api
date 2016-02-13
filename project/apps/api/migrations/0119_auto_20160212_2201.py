# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0118_auto_20160212_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Qualified'), (20, b'Did Not Qualify'), (30, b'Disqualified'), (40, b'Dropped'), (60, b'Ranked'), (90, b'Final')]),
        ),
    ]
