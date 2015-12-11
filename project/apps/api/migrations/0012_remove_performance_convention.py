# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20151211_1038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='convention',
        ),
    ]
