# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20151009_0536'),
    ]

    operations = [
        migrations.RenameField(
            model_name='score',
            old_name='score',
            new_name='points',
        ),
    ]
