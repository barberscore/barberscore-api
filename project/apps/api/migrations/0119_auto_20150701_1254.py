# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0118_auto_20150701_1246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contestant',
            name='baritone',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='bass',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='director',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='lead',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='tenor',
        ),
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
            name='director',
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
