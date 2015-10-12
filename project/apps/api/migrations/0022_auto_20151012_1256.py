# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20151012_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New')]),
        ),
        migrations.AddField(
            model_name='judge',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New')]),
        ),
        migrations.AddField(
            model_name='performance',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New')]),
        ),
        migrations.AddField(
            model_name='score',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New')]),
        ),
    ]
