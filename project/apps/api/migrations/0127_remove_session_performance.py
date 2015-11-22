# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0126_auto_20151121_2331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='performance',
        ),
    ]
