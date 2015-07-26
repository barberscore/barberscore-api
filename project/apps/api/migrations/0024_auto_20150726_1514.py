# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_auto_20150725_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='spot',
            name='person_match',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='spot',
            name='song_match',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
