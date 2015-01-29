# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_convention_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapter',
            options={},
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='blurb',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='email',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='facebook',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='location',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='picture',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='twitter',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='website',
        ),
    ]
