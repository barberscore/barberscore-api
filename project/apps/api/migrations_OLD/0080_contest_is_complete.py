# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0079_contest_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
    ]
