# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0140_auto_20151201_0811'),
    ]

    operations = [
        migrations.AddField(
            model_name='panel',
            name='rounds',
            field=models.IntegerField(blank=True, help_text=b'\n            Number of rounds', null=True, choices=[(3, 3), (2, 2), (1, 1)]),
        ),
        migrations.AddField(
            model_name='panel',
            name='size',
            field=models.IntegerField(blank=True, help_text=b'\n            Size of the judging panel (typically three or five.)', null=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]),
        ),
    ]
