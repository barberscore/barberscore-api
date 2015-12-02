# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_auto_20151018_1500'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contestant',
            name='finals_place',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_place',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_place',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_score',
        ),
        migrations.AddField(
            model_name='performance',
            name='status_monitor',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, help_text=b'Status last updated', monitor=b'status'),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='draw',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='mus_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='mus_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='prs_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='prs_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='sng_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='sng_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='total_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='total_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='mus_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='mus_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='prs_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='prs_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='sng_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='sng_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (1, b'Ready'), (2, b'Current'), (1, b'Complete')]),
        ),
        migrations.AlterField(
            model_name='performance',
            name='total_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='total_score',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
