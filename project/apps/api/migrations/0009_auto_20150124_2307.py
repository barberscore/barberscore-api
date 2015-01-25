# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20150124_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='quartetperformance',
            name='appearance',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quartetperformance',
            name='mus1',
            field=models.IntegerField(help_text=b'\n            The raw music score of the first song.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quartetperformance',
            name='mus2',
            field=models.IntegerField(help_text=b'\n            The raw music score of the second song.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quartetperformance',
            name='prs1',
            field=models.IntegerField(help_text=b'\n            The raw presentation score of the first song.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quartetperformance',
            name='prs2',
            field=models.IntegerField(help_text=b'\n            The raw presentation score of the second song.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quartetperformance',
            name='sng1',
            field=models.IntegerField(help_text=b'\n            The raw singing score of the first song.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quartetperformance',
            name='sng2',
            field=models.IntegerField(help_text=b'\n            The raw singing score of the second song.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quartetperformance',
            name='song1',
            field=models.CharField(help_text=b'\n            The title of the first song of the performance.', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quartetperformance',
            name='song2',
            field=models.CharField(help_text=b'\n            The title of the second song of the performance.', max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
