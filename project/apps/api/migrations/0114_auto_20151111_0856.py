# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0113_auto_20151111_0855'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='end',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='start',
            new_name='start_date',
        ),
        migrations.RenameField(
            model_name='organization',
            old_name='end',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='organization',
            old_name='start',
            new_name='start_date',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='end',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='start',
            new_name='start_date',
        ),
    ]
