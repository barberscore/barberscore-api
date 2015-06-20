# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0077_auto_20150619_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='convention',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
