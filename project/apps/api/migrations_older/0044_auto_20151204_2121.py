# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0043_remove_song_penalty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='penalty',
        ),
        migrations.AlterField(
            model_name='performance',
            name='name',
            field=models.CharField(unique=True, max_length=255, editable=False),
        ),
    ]
