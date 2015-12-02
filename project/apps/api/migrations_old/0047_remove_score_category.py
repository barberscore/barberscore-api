# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0046_auto_20151021_0936'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='score',
            name='category',
        ),
    ]
