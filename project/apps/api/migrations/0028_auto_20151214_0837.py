# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_auto_20151214_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='num_rounds',
            field=models.IntegerField(default=1, help_text=b'\n            Number of rounds (rounds) for the session.', null=True, blank=True, choices=[(3, 3), (2, 2), (1, 1)]),
        ),
    ]
