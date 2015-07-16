# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0125_auto_20150703_2013'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Director',
        ),
        migrations.DeleteModel(
            name='Judge',
        ),
        migrations.AlterUniqueTogether(
            name='note',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='note',
            name='performance',
        ),
        migrations.RemoveField(
            model_name='note',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='performance',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='performance',
            name='contestant',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='title1',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='title2',
        ),
        migrations.DeleteModel(
            name='Singer',
        ),
        migrations.RemoveField(
            model_name='group',
            name='bsmdb_id',
        ),
        migrations.DeleteModel(
            name='Note',
        ),
        migrations.DeleteModel(
            name='Performance',
        ),
    ]
