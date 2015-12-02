# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0091_auto_20151029_1315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='fuzzy',
        ),
        migrations.RemoveField(
            model_name='person',
            name='fuzzy',
        ),
        migrations.RemoveField(
            model_name='tune',
            name='fuzzy',
        ),
    ]
