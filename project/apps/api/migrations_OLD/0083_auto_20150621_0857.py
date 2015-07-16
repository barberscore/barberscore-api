# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0082_auto_20150621_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='arrangement',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
