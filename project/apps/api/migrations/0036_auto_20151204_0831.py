# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_auto_20151203_2115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='judge',
        ),
        migrations.RemoveField(
            model_name='person',
            name='judge_monitor',
        ),
    ]
