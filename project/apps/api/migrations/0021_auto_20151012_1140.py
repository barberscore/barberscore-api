# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_contest_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='is_complete',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='is_place',
        ),
        migrations.AlterField(
            model_name='contest',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (1, b'Upcoming'), (2, b'Current'), (3, b'Reviewing'), (4, b'Complete')]),
        ),
    ]
