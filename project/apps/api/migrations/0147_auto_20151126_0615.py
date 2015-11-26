# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0146_auto_20151126_0612'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contestant',
            name='men',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='mus_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='mus_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='prs_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='prs_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='sng_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='sng_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='total_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='total_score',
        ),
    ]
