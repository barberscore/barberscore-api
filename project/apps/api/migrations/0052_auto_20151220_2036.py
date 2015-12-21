# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0051_auto_20151219_1837'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chapter',
            old_name='dates',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='dates',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='dates',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='group',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='group',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='person',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='person',
            name='start_date',
        ),
    ]
