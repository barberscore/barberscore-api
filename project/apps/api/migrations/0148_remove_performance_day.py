# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0147_auto_20151201_1134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='day',
        ),
    ]
