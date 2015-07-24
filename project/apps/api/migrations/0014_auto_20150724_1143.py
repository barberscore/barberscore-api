# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20150724_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arranger',
            name='chart',
            field=models.ForeignKey(related_name='arrangers', blank=True, to='api.Chart', null=True),
        ),
        migrations.AlterField(
            model_name='arranger',
            name='person',
            field=models.ForeignKey(related_name='arrangements', blank=True, to='api.Person', null=True),
        ),
    ]
