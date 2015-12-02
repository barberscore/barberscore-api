# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0069_auto_20151025_2030'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Appearance',
            new_name='Performance',
        ),
        migrations.RenameField(
            model_name='song',
            old_name='appearance',
            new_name='performance',
        ),
    ]
