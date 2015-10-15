# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0049_auto_20151015_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='arranger',
            field=models.ForeignKey(related_name='performances', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='song',
            field=models.ForeignKey(related_name='performances', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
    ]
