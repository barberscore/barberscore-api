# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0112_auto_20150628_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='is_place',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contest',
            name='is_score',
            field=models.BooleanField(default=False),
        ),
    ]
