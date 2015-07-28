# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_auto_20150727_1320'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spot',
            old_name='person',
            new_name='arranger',
        ),
    ]
