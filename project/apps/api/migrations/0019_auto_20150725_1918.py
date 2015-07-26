# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20150725_1416'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.CharField(max_length=200)),
                ('is_flag', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Duplicate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_id', models.CharField(max_length=200)),
                ('collection', models.ForeignKey(related_name='duplicates', to='api.Collection')),
            ],
        ),
        migrations.CreateModel(
            name='GroupF',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('child', models.CharField(max_length=200)),
                ('parent', models.ForeignKey(to='api.Group')),
            ],
        ),
        migrations.CreateModel(
            name='PersonF',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('child', models.CharField(max_length=200)),
                ('parent', models.ForeignKey(to='api.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Primitive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('trainer', jsonfield.fields.JSONField(null=True, blank=True)),
                ('training_file', models.FileField(null=True, upload_to=b'', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SongF',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('child', models.CharField(max_length=200)),
                ('parent', models.ForeignKey(to='api.Song')),
            ],
        ),
        migrations.AddField(
            model_name='collection',
            name='primitive',
            field=models.ForeignKey(related_name='collections', to='api.Primitive'),
        ),
    ]
