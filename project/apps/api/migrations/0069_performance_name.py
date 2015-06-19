# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0068_contestant_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
