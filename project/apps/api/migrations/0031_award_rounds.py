# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_auto_20151214_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='rounds',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
