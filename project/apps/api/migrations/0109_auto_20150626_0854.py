# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0108_auto_20150626_0835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contestant',
            name='finals_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_score',
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_mus1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_mus1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_mus2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_mus2_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_prs1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_prs1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_prs2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_prs2_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_sng1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_sng1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_sng2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_sng2_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_song1',
            field=models.ForeignKey(related_name='contestants_f1', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_song1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_song1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_song2',
            field=models.ForeignKey(related_name='contestants_f2', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_song2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_song2_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_mus1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_mus1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_mus2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_mus2_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_prs1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_prs1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_prs2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_prs2_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_sng1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_sng1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_sng2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_sng2_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_song1',
            field=models.ForeignKey(related_name='contestants_q1', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_song1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_song1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_song2',
            field=models.ForeignKey(related_name='contestants_q2', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_song2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_song2_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_mus1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_mus1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_mus2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_mus2_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_prs1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_prs1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_prs2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_prs2_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_sng1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_sng1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_sng2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_sng2_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_song1',
            field=models.ForeignKey(related_name='contestants_s1', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_song1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_song1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_song2',
            field=models.ForeignKey(related_name='contestants_s2', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_song2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_song2_score',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
