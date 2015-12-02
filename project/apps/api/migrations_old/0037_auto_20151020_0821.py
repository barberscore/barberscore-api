# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_appearance_position'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appearance',
            options={'ordering': ['session', 'position', 'contestant']},
        ),
        migrations.RemoveField(
            model_name='appearance',
            name='draw',
        ),
        migrations.AlterField(
            model_name='appearance',
            name='position',
            field=models.PositiveSmallIntegerField(null=True, verbose_name=b'Position'),
        ),
    ]
