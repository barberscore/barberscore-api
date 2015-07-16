# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0124_auto_20150703_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='quarters_song1_arranger',
            field=models.ForeignKey(related_name='contestants_quarters_song1_arranger', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_song2_arranger',
            field=models.ForeignKey(related_name='contestants_quarters_song2_arranger', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_song1_arranger',
            field=models.ForeignKey(related_name='contestants_semis_song1_arranger', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_song2_arranger',
            field=models.ForeignKey(related_name='contestants_semis_song2_arranger', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='finals_song1',
            field=models.ForeignKey(related_name='contestants_finals_song1', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='finals_song2',
            field=models.ForeignKey(related_name='contestants_finals_song2', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='quarters_song1',
            field=models.ForeignKey(related_name='contestants_quarters_song1', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='quarters_song2',
            field=models.ForeignKey(related_name='contestants_quarters_song2', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='semis_song1',
            field=models.ForeignKey(related_name='contestants_semis_song1', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='semis_song2',
            field=models.ForeignKey(related_name='contestants_semis_song2', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
    ]
