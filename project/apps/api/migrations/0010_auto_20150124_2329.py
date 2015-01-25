# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20150124_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='chorusperformance',
            name='appearance',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chorusperformance',
            name='mus1',
            field=models.IntegerField(help_text=b'\n            The raw music score of the first song.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chorusperformance',
            name='mus2',
            field=models.IntegerField(help_text=b'\n            The raw music score of the second song.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chorusperformance',
            name='prs1',
            field=models.IntegerField(help_text=b'\n            The raw presentation score of the first song.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chorusperformance',
            name='prs2',
            field=models.IntegerField(help_text=b'\n            The raw presentation score of the second song.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chorusperformance',
            name='sng1',
            field=models.IntegerField(help_text=b'\n            The raw singing score of the first song.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chorusperformance',
            name='sng2',
            field=models.IntegerField(help_text=b'\n            The raw singing score of the second song.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chorusperformance',
            name='song1',
            field=models.CharField(help_text=b'\n            The title of the first song of the performance.', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chorusperformance',
            name='song2',
            field=models.CharField(help_text=b'\n            The title of the second song of the performance.', max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
