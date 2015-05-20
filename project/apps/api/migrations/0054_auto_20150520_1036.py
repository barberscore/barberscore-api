# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0053_contestant_stagetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='finals_place',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_place',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='queue',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_place',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_score',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
