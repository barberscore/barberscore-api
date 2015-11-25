# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0138_auto_20151125_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='entrant',
            field=models.ForeignKey(related_name='performances', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Entrant', null=True),
        ),
    ]
