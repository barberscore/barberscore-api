# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0055_auto_20151021_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (1, b'Ready'), (2, b'Current'), (3, b'Complete')]),
        ),
    ]
