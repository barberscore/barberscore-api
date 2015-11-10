# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0106_auto_20151109_1325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='state',
        ),
    ]
