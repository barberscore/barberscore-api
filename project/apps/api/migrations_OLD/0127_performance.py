# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0126_auto_20150705_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, populate_from=b'name', null=True, editable=False, blank=True)),
                ('round', models.IntegerField(default=3, null=True, blank=True, choices=[(1, b'Finals'), (2, b'Semis'), (3, b'Quarters')])),
                ('order', models.IntegerField(blank=True, null=True, choices=[(1, b'1'), (2, b'2')])),
                ('mus_points', models.IntegerField(null=True, blank=True)),
                ('prs_points', models.IntegerField(null=True, blank=True)),
                ('sng_points', models.IntegerField(null=True, blank=True)),
                ('total_points', models.IntegerField(null=True, blank=True)),
                ('mus_score', models.FloatField(null=True, blank=True)),
                ('prs_score', models.FloatField(null=True, blank=True)),
                ('sng_score', models.FloatField(null=True, blank=True)),
                ('total_score', models.FloatField(null=True, blank=True)),
                ('penalty', models.TextField(null=True, blank=True)),
                ('arranger', models.ForeignKey(related_name='performances', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True)),
                ('contestant', models.ForeignKey(related_name='performances', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Contestant', null=True)),
                ('song', models.ForeignKey(related_name='performances', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True)),
            ],
        ),
    ]
