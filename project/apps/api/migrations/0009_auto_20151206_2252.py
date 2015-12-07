# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_person_is_judge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certification',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (1, b'Active'), (2, b'Candidate'), (3, b'Inactive')]),
        ),
    ]
