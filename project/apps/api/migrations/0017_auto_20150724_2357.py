# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_spot'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='spot',
            field=models.ForeignKey(related_name='performances', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Spot', null=True),
        ),
        migrations.AddField(
            model_name='spot',
            name='fuzzy',
            field=models.TextField(null=True, blank=True),
        ),
    ]
