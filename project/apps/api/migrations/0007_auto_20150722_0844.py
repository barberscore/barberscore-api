# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20150722_0840'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arranger',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('part', models.IntegerField(default=1, choices=[(1, b'Arranger'), (2, b'Co-Arranger')])),
            ],
        ),
        migrations.AlterField(
            model_name='chart',
            name='arranger_OLD',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='chart',
            name='arrangers_OLD',
            field=models.ManyToManyField(related_name='charts_OLD', to='api.Person', blank=True),
        ),
        migrations.AlterField(
            model_name='chart',
            name='song',
            field=models.ForeignKey(to='api.Song'),
        ),
        migrations.AlterField(
            model_name='chart',
            name='songs',
            field=models.ManyToManyField(related_name='charts', to='api.Song', blank=True),
        ),
        migrations.AddField(
            model_name='arranger',
            name='chart',
            field=models.ForeignKey(related_name='arrangers', to='api.Chart'),
        ),
        migrations.AddField(
            model_name='arranger',
            name='person',
            field=models.ForeignKey(related_name='charts', to='api.Person'),
        ),
        migrations.AlterUniqueTogether(
            name='arranger',
            unique_together=set([('chart', 'person')]),
        ),
    ]
