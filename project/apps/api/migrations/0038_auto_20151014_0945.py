# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_auto_20151014_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='points',
            field=models.IntegerField(help_text=b'\n            Total raw points for this contestant (cumuative).', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='score',
            field=models.FloatField(help_text=b'\n            The percentile of the total points (cumulative , all rounds).', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='judge',
            name='person',
            field=models.ForeignKey(related_name='contests', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='mus_points',
            field=models.IntegerField(help_text=b'\n            The total music points for this performance.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='mus_score',
            field=models.FloatField(help_text=b'\n            The percentile music score for this performance.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='penalty',
            field=models.TextField(help_text=b'\n            Free form for penalties (notes).', blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='prs_points',
            field=models.IntegerField(help_text=b'\n            The total presentation points for this performance.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='prs_score',
            field=models.FloatField(help_text=b'\n            The percentile presentation score for this performance.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='sng_points',
            field=models.IntegerField(help_text=b'\n            The total singing points for this performance.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='sng_score',
            field=models.FloatField(help_text=b'\n            The percentile singing score for this performance.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='total_points',
            field=models.IntegerField(help_text=b'\n            The total points for this performance.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='total_score',
            field=models.FloatField(help_text=b'\n            The total percentile score for this performance.', null=True, blank=True),
        ),
    ]
