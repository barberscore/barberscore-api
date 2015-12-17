# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0041_auto_20151216_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Active'), (20, b'Inactive'), (50, b'Duplicate')]),
        ),
        migrations.AlterField(
            model_name='group',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (10, b'Active'), (20, b'Inactive'), (50, b'Duplicate')]),
        ),
    ]
