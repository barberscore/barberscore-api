# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0147_auto_20150714_2139'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('arranger', models.ForeignKey(related_name='charts', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True)),
                ('song', models.ForeignKey(related_name='charts', to='api.Song')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
