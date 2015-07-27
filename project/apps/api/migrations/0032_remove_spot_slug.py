# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_auto_20150727_1208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spot',
            name='slug',
        ),
    ]
