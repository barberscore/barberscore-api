# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_auto_20150727_2047'),
    ]

    operations = [
        migrations.RenameField(
            model_name='performance',
            old_name='spot',
            new_name='arrangement',
        ),
    ]
