# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_auto_20150128_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quartet',
            name='members',
            field=models.ManyToManyField(related_name='quartets', through='api.QuartetMember', to='api.Singer'),
            preserve_default=True,
        ),
    ]
