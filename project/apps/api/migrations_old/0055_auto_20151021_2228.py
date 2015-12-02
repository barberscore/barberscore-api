# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0054_auto_20151021_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='points',
            field=models.IntegerField(help_text=b'\n            The number of points awarded (0-100)', null=True, blank=True),
        ),
    ]
