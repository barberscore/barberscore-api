# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0153_score_performance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='score',
            name='performance',
        ),
    ]
