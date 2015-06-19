# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0067_auto_20150618_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
