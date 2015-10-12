# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20151012_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='is_active',
            field=models.BooleanField(default=False, help_text=b'\n            A global boolean that controls if the resource is accessible via the API'),
        ),
        migrations.AlterField(
            model_name='convention',
            name='is_active',
            field=models.BooleanField(default=False, help_text=b'\n            A global boolean that controls if the resource is accessible via the API'),
        ),
    ]
