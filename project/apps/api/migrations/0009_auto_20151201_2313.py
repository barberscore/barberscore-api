# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20151201_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ranking',
            name='contest',
            field=models.ForeignKey(related_name='rankings', to='api.Contest'),
        ),
    ]
