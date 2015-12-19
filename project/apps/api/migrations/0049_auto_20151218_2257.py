# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0048_auto_20151218_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='rounds',
            field=models.IntegerField(),
        ),
    ]
