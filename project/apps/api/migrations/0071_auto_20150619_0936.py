# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0070_auto_20150619_0740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='convention',
            field=models.ForeignKey(related_name='contests', blank=True, to='api.Convention', null=True),
        ),
    ]
