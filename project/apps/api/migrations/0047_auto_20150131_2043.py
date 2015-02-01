# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0046_auto_20150131_1553'),
    ]

    operations = [
        migrations.CreateModel(
            name='Finish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('place', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49)])),
                ('prelim', models.FloatField(null=True, blank=True)),
                ('seed', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49)])),
                ('score', models.FloatField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChorusFinish',
            fields=[
                ('finish_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='api.Finish')),
                ('chorus', models.ForeignKey(related_name='finishes', blank=True, to='api.Chorus', null=True)),
            ],
            options={
                'verbose_name_plural': 'Chorus Finishes',
            },
            bases=('api.finish',),
        ),
        migrations.CreateModel(
            name='QuartetFinish',
            fields=[
                ('finish_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='api.Finish')),
                ('quartet', models.ForeignKey(related_name='finishes', blank=True, to='api.Quartet', null=True)),
            ],
            options={
                'verbose_name_plural': 'Quartet Finishes',
            },
            bases=('api.finish',),
        ),
        migrations.AddField(
            model_name='finish',
            name='contest',
            field=models.ForeignKey(blank=True, to='api.Contest', null=True),
            preserve_default=True,
        ),
    ]
