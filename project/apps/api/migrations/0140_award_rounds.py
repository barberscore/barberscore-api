# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0139_auto_20151130_0914'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='rounds',
            field=models.IntegerField(blank=True, help_text=b'\n            Number of rounds', null=True, choices=[(3, 3), (2, 2), (1, 1)]),
        ),
    ]
