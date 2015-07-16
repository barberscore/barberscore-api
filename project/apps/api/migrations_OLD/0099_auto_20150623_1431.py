# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0098_auto_20150623_1423'),
    ]

    operations = [
        migrations.RenameField(
            model_name='performance',
            old_name='mus1_rata',
            new_name='mus1_score',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='mus2_rata',
            new_name='mus2_score',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='prs1_rata',
            new_name='prs1_score',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='prs2_rata',
            new_name='prs2_score',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='sng1_rata',
            new_name='sng1_score',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='sng2_rata',
            new_name='sng2_score',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='song1_raw',
            new_name='song1_points',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='song1_rata',
            new_name='song1_score',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='song2_raw',
            new_name='song2_points',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='song2_rata',
            new_name='song2_score',
        ),
    ]
