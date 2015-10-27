# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0074_catalog_song_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='arranger',
            field=models.CharField(max_length=255, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='song',
            name='title',
            field=models.CharField(max_length=255, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='arranger',
            name='song',
            field=models.ForeignKey(related_name='foos', blank=True, to='api.Song', null=True),
        ),
    ]
