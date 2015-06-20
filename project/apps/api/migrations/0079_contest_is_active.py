# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0078_convention_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
