# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0057_auto_20151015_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arranger',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('part', models.IntegerField(default=1, choices=[(1, b'Arranger'), (2, b'Co-Arranger')])),
                ('performance', models.ForeignKey(to='api.Performance')),
                ('person', models.ForeignKey(to='api.Person')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='arranger',
            unique_together=set([('performance', 'person')]),
        ),
    ]
