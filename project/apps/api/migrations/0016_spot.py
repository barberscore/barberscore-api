# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_catalog_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='Spot',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('bhs_id', models.IntegerField(null=True, blank=True)),
                ('bhs_published', models.DateField(null=True, blank=True)),
                ('bhs_songname', models.CharField(max_length=200, null=True, blank=True)),
                ('bhs_arranger', models.CharField(max_length=200, null=True, blank=True)),
                ('bhs_fee', models.FloatField(null=True, blank=True)),
                ('bhs_difficulty', models.IntegerField(blank=True, null=True, choices=[(1, b'Very Easy'), (2, b'Easy'), (3, b'Medium'), (4, b'Hard'), (5, b'Very Hard')])),
                ('bhs_tempo', models.IntegerField(blank=True, null=True, choices=[(1, b'Ballad'), (2, b'Uptune'), (3, b'Mixed')])),
                ('bhs_medley', models.BooleanField(default=False)),
                ('is_parody', models.BooleanField(default=False)),
                ('is_medley', models.BooleanField(default=False)),
                ('person', models.ForeignKey(related_name='spots', blank=True, to='api.Person', null=True)),
                ('song', models.ForeignKey(related_name='spots', blank=True, to='api.Song', null=True)),
            ],
        ),
    ]
