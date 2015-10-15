# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0046_auto_20151015_0811'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('start', models.DateTimeField(null=True, verbose_name='start', blank=True)),
                ('end', models.DateTimeField(null=True, verbose_name='end', blank=True)),
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(help_text=b'\n            The name of the event (determined programmatically.)', unique=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('draw', models.IntegerField(help_text=b'\n            The OA (Order of Appearance) in the contest schedule.  Specific to each round/session.', null=True, blank=True)),
                ('kind', models.IntegerField(help_text=b'\n            The kind of event.', choices=[(b'Session', [(1, b'Finals'), (2, b'Semis'), (3, b'Quarters')]), (b'Other', [(4, b'Other')])])),
                ('location', models.CharField(help_text=b'\n            The location of the event.', max_length=200, blank=True)),
                ('is_active', models.BooleanField(default=False, help_text=b'\n            A global boolean that controls if the resource is accessible via the API')),
                ('contest', models.ForeignKey(related_name='events', on_delete=django.db.models.deletion.SET_NULL, to='api.Contest', help_text=b'\n            The contest associated with this event.', null=True)),
                ('contestant', models.ForeignKey(related_name='events', on_delete=django.db.models.deletion.SET_NULL, to='api.Contestant', help_text=b'\n            The contestant associated with this event.', null=True)),
                ('convention', models.ForeignKey(related_name='events', to='api.Convention', help_text=b'\n            The convention at which this event occurs.')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
