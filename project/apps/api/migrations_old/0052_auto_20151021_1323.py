# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0051_auto_20151021_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='history',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (10, b'Scoresheet'), (40, b'CSV'), (40, b'Incomplete'), (50, b'Complete')]),
        ),
    ]
