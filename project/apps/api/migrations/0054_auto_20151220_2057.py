# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0053_auto_20151220_2056'),
    ]

    operations = [
        migrations.RenameField(
            model_name='convention',
            old_name='dates2',
            new_name='date',
        ),
    ]
