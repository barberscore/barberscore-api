# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20150722_1041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chart',
            name='song',
        ),
    ]
