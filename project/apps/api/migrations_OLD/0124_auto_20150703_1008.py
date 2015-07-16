# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0123_remove_contest_is_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='finals_song1_arranger',
            field=models.ForeignKey(related_name='contestants_f1_arranger', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_song2_arranger',
            field=models.ForeignKey(related_name='contestants_f2_arranger', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
    ]
