# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20151012_0956'),
    ]

    operations = [
        migrations.RenameField(
            model_name='district',
            old_name='end_date',
            new_name='end',
        ),
        migrations.RenameField(
            model_name='district',
            old_name='start_date',
            new_name='start',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='end_date',
            new_name='end',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='start_date',
            new_name='start',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='end_date',
            new_name='end',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='start_date',
            new_name='start',
        ),
    ]
