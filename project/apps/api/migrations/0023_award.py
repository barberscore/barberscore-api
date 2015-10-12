# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20151012_1256'),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.IntegerField(choices=[(1, b'First Place Gold Medalist'), (2, b'First Place Silver Medalist'), (3, b'Third Place Bronze Medalist'), (4, b'Fourth Place Bronze Medalist'), (5, b'Fifth Place Bronze Medalist')])),
                ('contestant', models.ForeignKey(related_name='awards', to='api.Contestant')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
