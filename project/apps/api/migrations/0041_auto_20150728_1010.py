# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0040_auto_20150728_0950'),
    ]

    operations = [
        migrations.CreateModel(
            name='DuplicatePerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField()),
                ('child', models.ForeignKey(related_name='children', to='api.Person')),
                ('parent', models.ForeignKey(to='api.Person')),
            ],
        ),
        migrations.CreateModel(
            name='DuplicateSong',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField()),
                ('child', models.ForeignKey(related_name='children', to='api.Song')),
                ('parent', models.ForeignKey(to='api.Song')),
            ],
        ),
        migrations.RemoveField(
            model_name='personf',
            name='child',
        ),
        migrations.RemoveField(
            model_name='personf',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='songf',
            name='child',
        ),
        migrations.RemoveField(
            model_name='songf',
            name='parent',
        ),
        migrations.AlterField(
            model_name='duplicategroup',
            name='child',
            field=models.ForeignKey(related_name='children', to='api.Group'),
        ),
        migrations.AlterField(
            model_name='duplicategroup',
            name='score',
            field=models.IntegerField(),
        ),
        migrations.DeleteModel(
            name='PersonF',
        ),
        migrations.DeleteModel(
            name='SongF',
        ),
    ]
