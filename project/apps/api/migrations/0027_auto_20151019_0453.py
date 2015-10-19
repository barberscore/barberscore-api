# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20151019_0430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='panel',
            field=models.IntegerField(default=5, help_text=b'\n            Size of the judging panel (typically three or five.)', choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]),
        ),
    ]
