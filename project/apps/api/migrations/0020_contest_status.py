# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20151012_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (1, b'Upcoming'), (2, b'Current'), (3, b'Pending'), (4, b'Complete')]),
        ),
    ]
