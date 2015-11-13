# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0120_auto_20151112_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='panel',
            field=models.IntegerField(help_text=b'\n            Size of the judging panel (typically three or five.)', choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]),
        ),
        migrations.AlterField(
            model_name='contest',
            name='rounds',
            field=models.IntegerField(help_text=b'\n            Number of rounds', choices=[(3, 3), (2, 2), (1, 1)]),
        ),
    ]
