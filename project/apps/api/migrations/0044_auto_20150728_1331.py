# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0043_auto_20150728_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arrangement',
            name='arranger',
            field=models.ForeignKey(related_name='arrangements', blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='arrangement',
            name='song',
            field=models.ForeignKey(related_name='arrangements', blank=True, to='api.Song', null=True),
        ),
    ]
