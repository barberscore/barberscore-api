# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_chart_song'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bhs_id', models.IntegerField(null=True, blank=True)),
                ('bhs_published', models.DateField(null=True, blank=True)),
                ('bhs_arranger', models.CharField(max_length=200, null=True, blank=True)),
                ('bhs_fee', models.FloatField(null=True, blank=True)),
                ('bhs_difficulty', models.IntegerField(blank=True, null=True, choices=[(1, b'Very Easy'), (2, b'Easy'), (3, b'Medium'), (4, b'Hard'), (5, b'Very Hard')])),
                ('bhs_tempo', models.IntegerField(blank=True, null=True, choices=[(1, b'Ballad'), (2, b'Uptune'), (3, b'Mixed')])),
                ('bhs_medley', models.BooleanField(default=False)),
                ('song', models.ForeignKey(related_name='catalogs', blank=True, to='api.Song', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='arranger',
            name='catalog',
            field=models.ForeignKey(related_name='arrangers', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Catalog', null=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='catalog',
            field=models.ForeignKey(related_name='performances', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Catalog', null=True),
        ),
    ]
