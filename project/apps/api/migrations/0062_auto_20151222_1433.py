# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0061_auto_20151222_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judge',
            name='slot',
            field=models.IntegerField(),
        ),
    ]
