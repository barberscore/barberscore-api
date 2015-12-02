# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0060_auto_20151024_0445'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appearance',
            options={'ordering': ['session', 'position']},
        ),
        migrations.AlterField(
            model_name='contest',
            name='panel',
            field=models.IntegerField(default=5, help_text=b'\n            Size of the judging panel (typically three or five.)', null=True, blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]),
        ),
    ]
