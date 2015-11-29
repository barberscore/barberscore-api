# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0133_auto_20151128_1625'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ranking',
            name='contest',
        ),
    ]
