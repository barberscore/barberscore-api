# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20151205_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='is_judge',
            field=models.BooleanField(default=False),
        ),
    ]
