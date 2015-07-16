# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0048_auto_20150512_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='mus2_rata',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='prs1_rata',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='prs2_rata',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='sng1_rata',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='sng2_rata',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='song1_rata',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='song1_raw',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='song2_rata',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='song2_raw',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='total_rata',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='total_raw',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
    ]
