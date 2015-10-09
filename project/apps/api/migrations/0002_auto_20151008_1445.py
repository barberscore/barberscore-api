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
            name='Judge',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('part', models.IntegerField(choices=[(1, b'Music'), (2, b'Presentation'), (3, b'Singing'), (4, b'Administrator')])),
                ('contest', models.ForeignKey(related_name='judges', to='api.Contest')),
                ('person', models.ForeignKey(related_name='contests', to='api.Person')),
            ],
            options={
                'ordering': ('-name',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='judge',
            unique_together=set([('contest', 'person')]),
        ),
    ]
