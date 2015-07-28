# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0042_auto_20150728_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arrangement',
            name='arranger',
            field=models.ForeignKey(related_name='arrangements', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='arrangement',
            name='song',
            field=models.ForeignKey(related_name='arrangements', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
    ]
