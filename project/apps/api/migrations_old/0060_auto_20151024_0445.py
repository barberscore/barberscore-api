# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0059_appearance_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judge',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (10, b'Scheduled'), (20, b'Confirmed'), (30, b'Complete')]),
        ),
    ]
