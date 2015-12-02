# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20151202_0729'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='num',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
