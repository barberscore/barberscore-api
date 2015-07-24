# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20150724_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalog',
            name='bhs_songname',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
