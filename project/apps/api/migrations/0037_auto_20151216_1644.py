# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_auto_20151216_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='kind',
            field=models.IntegerField(choices=[(1, b'Finals'), (2, b'Semi-Finals'), (3, b'Quarter-Finals')]),
        ),
    ]
