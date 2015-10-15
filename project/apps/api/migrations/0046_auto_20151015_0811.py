# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_auto_20151014_1849'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('status', models.IntegerField(default=0, choices=[(0, b'New')])),
                ('kind', models.IntegerField(default=1, choices=[(1, b'Finals'), (2, b'Semis'), (3, b'Quarters')])),
                ('draw', models.IntegerField(help_text=b'\n            The OA (Order of Appearance) in the contest schedule.  Specific to each round/session.')),
                ('stagetime', models.DateTimeField(help_text=b"\n            The estimated stagetime (may be replaced by 'start' in later versions).", null=True, blank=True)),
                ('contest', models.ForeignKey(related_name='sessions', to='api.Contest')),
                ('contestant', models.ForeignKey(related_name='sessions', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Contestant', null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='session',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='session',
            name='contest',
        ),
        migrations.RemoveField(
            model_name='session',
            name='contestant',
        ),
        migrations.DeleteModel(
            name='Session',
        ),
    ]
