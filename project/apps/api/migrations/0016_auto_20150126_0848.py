# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20150126_0843'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quartetperformance',
            options={'ordering': ['round', 'quartet']},
        ),
        migrations.AlterField(
            model_name='chorusperformance',
            name='round',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Finals'), (2, b'Semi-Finals'), (3, b'Quarter-Finals')]),
            preserve_default=True,
        ),
    ]
