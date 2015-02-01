# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import django_pg.models.fields.uuid
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_auto_20150130_1045'),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', django_pg.models.fields.uuid.UUIDField(default=uuid.uuid4, unique=True, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(help_text=b'\n            The name of the award.  Must be unique.', unique=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('description', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuartetAward',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('award', models.ForeignKey(to='api.Award')),
                ('contest', models.ForeignKey(to='api.Contest')),
                ('quartet', models.ForeignKey(to='api.Quartet')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='quartetperformance',
            options={'ordering': ['contest', '-round', 'quartet']},
        ),
        migrations.AddField(
            model_name='quartet',
            name='awards',
            field=models.ManyToManyField(related_name='quartets', through='api.QuartetAward', to='api.Award'),
            preserve_default=True,
        ),
    ]
