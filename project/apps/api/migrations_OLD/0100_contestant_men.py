# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0099_auto_20150623_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='men',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
