# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0094_auto_20150623_0938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='baritone',
        ),
        migrations.RemoveField(
            model_name='group',
            name='bass',
        ),
        migrations.RemoveField(
            model_name='group',
            name='lead',
        ),
        migrations.RemoveField(
            model_name='group',
            name='tenor',
        ),
    ]
