# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20151018_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='men',
            field=models.IntegerField(default=4, help_text=b'\n            The number of men on stage (only for chourses).', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='mus_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='mus_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='prs_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='prs_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='sng_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='sng_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='total_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='total_score',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
