# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0056_auto_20151015_1623'),
    ]

    operations = [
        migrations.RenameField(
            model_name='performance',
            old_name='arranger',
            new_name='person',
        ),
    ]
