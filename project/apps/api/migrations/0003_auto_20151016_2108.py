# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20151016_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='mus_points',
            field=models.IntegerField(help_text=b'\n            The total music points for this appearance.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='mus_score',
            field=models.FloatField(help_text=b'\n            The percentile music score for this appearance.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='prs_points',
            field=models.IntegerField(help_text=b'\n            The total presentation points for this appearance.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='prs_score',
            field=models.FloatField(help_text=b'\n            The percentile presentation score for this appearance.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='sng_points',
            field=models.IntegerField(help_text=b'\n            The total singing points for this appearance.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='sng_score',
            field=models.FloatField(help_text=b'\n            The percentile singing score for this appearance.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='total_points',
            field=models.IntegerField(help_text=b'\n            The total points for this appearance.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='total_score',
            field=models.FloatField(help_text=b'\n            The total percentile score for this appearance.', null=True, blank=True),
        ),
    ]
