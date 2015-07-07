# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0132_auto_20150707_0354'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContestantSinger',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('part', models.IntegerField(blank=True, null=True, choices=[(1, b'Tenor'), (2, b'Lead'), (3, b'Baritone'), (4, b'Bass')])),
            ],
        ),
        migrations.AlterField(
            model_name='contestant',
            name='directors',
            field=models.ManyToManyField(related_name='contestants_d', to='api.Person'),
        ),
        migrations.AddField(
            model_name='contestantsinger',
            name='contestant',
            field=models.ForeignKey(to='api.Contestant'),
        ),
        migrations.AddField(
            model_name='contestantsinger',
            name='singer',
            field=models.ForeignKey(to='api.Person'),
        ),
        migrations.AddField(
            model_name='contestant',
            name='singers',
            field=models.ManyToManyField(related_name='contestants_s', through='api.ContestantSinger', to='api.Person'),
        ),
    ]
