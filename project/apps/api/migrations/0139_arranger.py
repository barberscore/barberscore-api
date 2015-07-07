# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0138_auto_20150707_0942'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arranger',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, populate_from=b'name', null=True, editable=False, blank=True)),
                ('part', models.IntegerField(default=1, null=True, blank=True, choices=[(1, b'Arranger')])),
                ('contestant', models.ForeignKey(related_name='arrangers', blank=True, to='api.Contestant', null=True)),
                ('person', models.ForeignKey(related_name='arrangers', blank=True, to='api.Person', null=True)),
            ],
        ),
    ]
