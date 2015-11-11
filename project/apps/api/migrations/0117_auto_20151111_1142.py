# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0116_auto_20151111_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Qualified'), (20, b'Accepted'), (30, b'Declined'), (40, b'Dropped'), (50, b'Official'), (60, b'Finished'), (90, b'Final')]),
        ),
    ]
