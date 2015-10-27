# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0072_arranger_catalog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='mus_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='mus_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='prs_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='prs_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='sng_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='sng_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='total_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='total_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='mus_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='mus_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='prs_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='prs_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='sng_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='sng_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='total_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='total_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='mus_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='mus_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='prs_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='prs_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='sng_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='sng_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='total_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='total_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
    ]
