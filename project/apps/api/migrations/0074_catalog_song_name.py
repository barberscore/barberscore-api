# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0073_auto_20151027_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalog',
            name='song_name',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
