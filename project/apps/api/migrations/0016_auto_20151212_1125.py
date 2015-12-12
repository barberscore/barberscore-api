# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20151212_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='long_name',
            field=models.CharField(max_length=200),
        ),
    ]
