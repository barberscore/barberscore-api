# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0159_auto_20151201_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='panelist',
            field=models.ForeignKey(related_name='scores', on_delete=django.db.models.deletion.SET_NULL, to='api.Panelist', null=True),
        ),
    ]
