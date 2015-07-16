# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20150421_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupmember',
            name='contest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Contest', null=True),
        ),
    ]
