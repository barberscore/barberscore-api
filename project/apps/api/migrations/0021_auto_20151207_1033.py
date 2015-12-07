# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20151207_1005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='chapter_code',
        ),
        migrations.RemoveField(
            model_name='group',
            name='chapter_name',
        ),
    ]
