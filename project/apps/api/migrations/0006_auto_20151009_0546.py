# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20151009_0541'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='judge',
            field=models.ForeignKey(related_name='scores', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Judge', null=True),
        ),
        migrations.AddField(
            model_name='score',
            name='performance',
            field=models.ForeignKey(related_name='scores', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Performance', null=True),
        ),
    ]
