# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0145_auto_20151126_0546'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrant',
            name='mus_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='entrant',
            name='mus_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='entrant',
            name='prs_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='entrant',
            name='prs_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='entrant',
            name='sng_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='entrant',
            name='sng_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='entrant',
            name='total_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='entrant',
            name='total_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
    ]
