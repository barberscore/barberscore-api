# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0086_auto_20150621_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='total_raw',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
