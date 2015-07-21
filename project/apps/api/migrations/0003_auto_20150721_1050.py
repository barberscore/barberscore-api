# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20150721_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='chart',
            name='arrangers',
            field=models.ManyToManyField(to='api.Person'),
        ),
        migrations.AddField(
            model_name='chart',
            name='songs',
            field=models.ManyToManyField(to='api.Song'),
        ),
    ]
