# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0042_auto_20151204_2102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='penalty',
        ),
    ]
