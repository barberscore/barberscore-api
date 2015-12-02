# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20151201_2313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='score',
            name='performance',
        ),
    ]
