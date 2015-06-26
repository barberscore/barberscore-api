# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0106_auto_20150625_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='title1',
            field=models.ForeignKey(related_name='performances_song1', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='title2',
            field=models.ForeignKey(related_name='performances_song2', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
    ]
