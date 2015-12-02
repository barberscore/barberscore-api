# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0155_score_perf'),
    ]

    operations = [
        migrations.RenameField(
            model_name='score',
            old_name='perf',
            new_name='performance',
        ),
    ]
