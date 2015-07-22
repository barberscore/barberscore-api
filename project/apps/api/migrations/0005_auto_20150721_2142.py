# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20150721_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chart',
            name='arrangers',
            field=models.ManyToManyField(to='api.Person', blank=True),
        ),
        migrations.AlterField(
            model_name='chart',
            name='songs',
            field=models.ManyToManyField(to='api.Song', blank=True),
        ),
    ]
