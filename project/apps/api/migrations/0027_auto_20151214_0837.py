# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20151214_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='size',
            field=models.IntegerField(blank=True, help_text=b'\n            Size of the judging panel (per category).', null=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]),
        ),
    ]
