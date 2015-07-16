# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0144_auto_20150714_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='convention',
            name='end',
            field=models.DateTimeField(null=True, verbose_name='end', blank=True),
        ),
        migrations.AddField(
            model_name='convention',
            name='start',
            field=models.DateTimeField(null=True, verbose_name='start', blank=True),
        ),
    ]
