# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'bbs', b'0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name=b'Contest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'year', models.CharField(max_length=4)),
                (b'contest_level', models.CharField(max_length=20, choices=[(b'International', b'International'), (b'CAR', b'CAR'), (b'CSD', b'CSD'), (b'DIX', b'DIX'), (b'EVG', b'EVG'), (b'FWD', b'FWD'), (b'ILL', b'ILL'), (b'JAD', b'JAD'), (b'LOL', b'LOL'), (b'MAD', b'MAD'), (b'NED', b'NED'), (b'NSC', b'NSC'), (b'ONT', b'ONT'), (b'PIO', b'PIO'), (b'RMD', b'RMD'), (b'SLD', b'SLD'), (b'SUN', b'SUN'), (b'SWD', b'SWD')])),
                (b'contest_type', models.CharField(max_length=20, choices=[(b'Quartet', b'Quartet Contest'), (b'Chorus', b'Chorus Contest'), (b'Collegiate', b'Collegiate Contest'), (b'Senior', b'Senior Contest')])),
                (b'slug', models.SlugField(unique=True, max_length=200)),
                (b'panel_size', models.IntegerField(default=5)),
            ],
            options={
                'ordering': [b'year', b'contest_level', b'contest_type'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Contestant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'name', models.CharField(max_length=200)),
                (b'slug', models.SlugField(unique=True, max_length=200)),
                (b'location', models.CharField(max_length=200, blank=True)),
                (b'website', models.URLField(blank=True)),
                (b'facebook', models.URLField(blank=True)),
                (b'phone', models.CharField(max_length=20, blank=True)),
                (b'director', models.CharField(max_length=200, blank=True)),
                (b'lead', models.CharField(max_length=200, blank=True)),
                (b'tenor', models.CharField(max_length=200, blank=True)),
                (b'baritone', models.CharField(max_length=200, blank=True)),
                (b'bass', models.CharField(max_length=200, blank=True)),
                (b'contestant_type', models.IntegerField(choices=[(1, b'Quartet'), (2, b'Chorus')])),
                (b'district', models.IntegerField(default=0, choices=[(0, b'Unknown'), (1, b'CAR'), (2, b'CSD'), (3, b'DIX'), (4, b'EVG'), (5, b'FWD'), (6, b'ILL'), (7, b'JAD'), (8, b'LOL'), (9, b'MAD'), (10, b'NED'), (11, b'NSC'), (12, b'ONT'), (13, b'PIO'), (14, b'RMD'), (15, b'SLD'), (16, b'SUN'), (17, b'SWD'), (18, b'BABS'), (19, b'NZABS'), (20, b'SNOBS'), (21, b'BHA')])),
                (b'prelim', models.FloatField(null=True, blank=True)),
            ],
            options={
                'ordering': [b'name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Score',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'contest', models.ForeignKey(to=b'bbs.Contest', to_field='id')),
                (b'contestant', models.ForeignKey(to=b'bbs.Contestant', to_field='id')),
                (b'contest_round', models.CharField(max_length=20, choices=[(b'Quarters', b'Quarter-Finals'), (b'Semis', b'Semi-Finals'), (b'Finals', b'Finals')])),
                (b'slug', models.SlugField(unique=True, max_length=200)),
                (b'song1', models.CharField(max_length=200)),
                (b'mus1', models.IntegerField()),
                (b'prs1', models.IntegerField()),
                (b'sng1', models.IntegerField()),
                (b'song2', models.CharField(max_length=200)),
                (b'mus2', models.IntegerField()),
                (b'prs2', models.IntegerField()),
                (b'sng2', models.IntegerField()),
                (b'men_on_stage', models.IntegerField(default=4, null=True)),
            ],
            options={
                'ordering': [b'contest', b'contest_round', b'contestant'],
            },
            bases=(models.Model,),
        ),
    ]
