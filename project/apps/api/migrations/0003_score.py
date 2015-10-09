# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20151008_1445'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('score', models.IntegerField(null=True, blank=True)),
                ('category', models.IntegerField(blank=True, null=True, choices=[(1, b'Music'), (2, b'Presentation'), (3, b'Singing'), (4, b'Admin')])),
                ('is_practice', models.BooleanField(default=False)),
            ],
        ),
    ]
