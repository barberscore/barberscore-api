# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appearance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('status', models.IntegerField(default=0, choices=[(0, b'New')])),
                ('session', models.IntegerField(choices=[(1, b'Finals'), (2, b'Semis'), (3, b'Quarters')])),
                ('mus_points', models.IntegerField(help_text=b'\n            The total music points for this appearance.', null=True, blank=True)),
                ('prs_points', models.IntegerField(help_text=b'\n            The total presentation points for this appearance.', null=True, blank=True)),
                ('sng_points', models.IntegerField(help_text=b'\n            The total singing points for this appearance.', null=True, blank=True)),
                ('total_points', models.IntegerField(help_text=b'\n            The total points for this appearance.', null=True, blank=True)),
                ('mus_score', models.FloatField(help_text=b'\n            The percentile music score for this appearance.', null=True, blank=True)),
                ('prs_score', models.FloatField(help_text=b'\n            The percentile presentation score for this appearance.', null=True, blank=True)),
                ('sng_score', models.FloatField(help_text=b'\n            The percentile singing score for this appearance.', null=True, blank=True)),
                ('total_score', models.FloatField(help_text=b'\n            The total percentile score for this appearance.', null=True, blank=True)),
                ('penalty', models.TextField(help_text=b'\n            Free form for penalties (notes).', blank=True)),
                ('contestant', models.ForeignKey(related_name='appearances', to='api.Contestant')),
            ],
            options={
                'ordering': ['contestant', 'session'],
            },
        ),
        migrations.AddField(
            model_name='performance',
            name='appearance',
            field=models.ForeignKey(related_name='performances', blank=True, to='api.Appearance', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='appearance',
            unique_together=set([('contestant', 'session')]),
        ),
    ]
