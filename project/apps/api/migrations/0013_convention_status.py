# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20151017_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='convention',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (1, b'Structured'), (2, b'Current'), (3, b'Complete')]),
        ),
    ]
