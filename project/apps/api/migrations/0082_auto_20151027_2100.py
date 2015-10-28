# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0081_auto_20151027_2000'),
    ]

    operations = [
        migrations.CreateModel(
            name='Winner',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('award', models.ForeignKey(related_name='winners', to='api.Person')),
                ('contestant', models.ForeignKey(related_name='winners', to='api.Contestant')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='award',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='award',
            name='contestant',
        ),
        migrations.RemoveField(
            model_name='award',
            name='kind',
        ),
        migrations.AlterUniqueTogether(
            name='winner',
            unique_together=set([('contestant', 'award')]),
        ),
    ]
