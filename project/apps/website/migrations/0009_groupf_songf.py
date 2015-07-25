# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20150725_1416'),
        ('website', '0008_personf'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupF',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('child', models.CharField(max_length=200)),
                ('parent', models.ForeignKey(related_name='parent_duplicates', to='api.Group')),
            ],
        ),
        migrations.CreateModel(
            name='SongF',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('child', models.CharField(max_length=200)),
                ('parent', models.ForeignKey(related_name='parent_duplicates', to='api.Song')),
            ],
        ),
    ]
