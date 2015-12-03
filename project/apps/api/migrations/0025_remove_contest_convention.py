# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20151203_1155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='convention',
        ),
    ]
