# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0054_auto_20150520_1036'),
    ]

    operations = [
        migrations.RenameField(
            model_name='performance',
            old_name='total_rata',
            new_name='score',
        ),
    ]
