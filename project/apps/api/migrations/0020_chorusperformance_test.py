# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20150126_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='chorusperformance',
            name='test',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
