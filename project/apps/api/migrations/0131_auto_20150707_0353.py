# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0130_auto_20150706_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='directors',
            field=models.ManyToManyField(related_name='groups', null=True, to='api.Person', blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='director',
            field=models.ForeignKey(related_name='groups_director', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
    ]
