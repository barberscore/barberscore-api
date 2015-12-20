# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0050_auto_20151219_0823'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapter',
            name='sts',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='sts_monitor',
        ),
        migrations.RemoveField(
            model_name='group',
            name='sts',
        ),
        migrations.RemoveField(
            model_name='group',
            name='sts_monitor',
        ),
        migrations.RemoveField(
            model_name='person',
            name='sts',
        ),
        migrations.RemoveField(
            model_name='person',
            name='sts_monitor',
        ),
    ]
