# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0094_auto_20151103_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='nick_name',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
