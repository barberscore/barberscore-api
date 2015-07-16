# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0061_auto_20150616_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='bsmdb_id',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
