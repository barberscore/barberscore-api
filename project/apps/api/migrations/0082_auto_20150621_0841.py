# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0081_song'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='title1',
            field=models.ForeignKey(related_name='performances_song1', blank=True, to='api.Song', null=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='title2',
            field=models.ForeignKey(related_name='performances_song2', blank=True, to='api.Song', null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='is_medley',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='song',
            name='is_parody',
            field=models.BooleanField(default=False),
        ),
    ]
