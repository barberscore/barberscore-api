# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20150724_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalog',
            name='person',
            field=models.ForeignKey(related_name='catalogs', blank=True, to='api.Person', null=True),
        ),
    ]
