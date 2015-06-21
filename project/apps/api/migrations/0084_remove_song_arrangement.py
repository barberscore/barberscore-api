# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0083_auto_20150621_0857'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='arrangement',
        ),
    ]
