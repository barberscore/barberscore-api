# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_auto_20150512_0916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='baritone_2',
        ),
        migrations.RemoveField(
            model_name='group',
            name='bass_2',
        ),
        migrations.RemoveField(
            model_name='group',
            name='lead_2',
        ),
        migrations.RemoveField(
            model_name='group',
            name='tenor_2',
        ),
    ]
