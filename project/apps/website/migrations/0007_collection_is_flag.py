# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_primitive_training_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='is_flag',
            field=models.BooleanField(default=False),
        ),
    ]
