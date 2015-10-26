# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0067_auto_20151025_1949'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Performance',
            new_name='Song',
        ),
        migrations.RenameField(
            model_name='arranger',
            old_name='performance',
            new_name='song',
        ),
        migrations.RenameField(
            model_name='score',
            old_name='performance',
            new_name='song',
        ),
    ]
