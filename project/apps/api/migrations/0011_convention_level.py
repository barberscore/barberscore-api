# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20151210_2303'),
    ]

    operations = [
        migrations.AddField(
            model_name='convention',
            name='level',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Convention'), (2, b'Session'), (3, b'Round')]),
        ),
    ]
