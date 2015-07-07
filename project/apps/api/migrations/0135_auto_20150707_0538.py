# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0134_auto_20150707_0451'),
    ]

    operations = [
        migrations.CreateModel(
            name='Singer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, populate_from=b'name', null=True, editable=False, blank=True)),
                ('part', models.IntegerField(blank=True, null=True, choices=[(1, b'Tenor'), (2, b'Lead'), (3, b'Baritone'), (4, b'Bass')])),
            ],
        ),
        migrations.RemoveField(
            model_name='contestantsinger',
            name='contestant',
        ),
        migrations.RemoveField(
            model_name='contestantsinger',
            name='singer',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='singers',
        ),
        migrations.DeleteModel(
            name='ContestantSinger',
        ),
        migrations.AddField(
            model_name='singer',
            name='contestant',
            field=models.ForeignKey(related_name='singers', to='api.Contestant'),
        ),
        migrations.AddField(
            model_name='singer',
            name='person',
            field=models.ForeignKey(to='api.Person'),
        ),
    ]
