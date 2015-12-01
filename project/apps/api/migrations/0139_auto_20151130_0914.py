# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0138_auto_20151129_0618'),
    ]

    operations = [
        migrations.AddField(
            model_name='ranking',
            name='mus_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='ranking',
            name='mus_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='ranking',
            name='place',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ranking',
            name='prs_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='ranking',
            name='prs_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='ranking',
            name='sng_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='ranking',
            name='sng_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='ranking',
            name='total_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='ranking',
            name='total_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
    ]
