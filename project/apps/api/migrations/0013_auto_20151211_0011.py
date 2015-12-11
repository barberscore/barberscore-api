# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20151211_0007'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='slots',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='session',
            name='start_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
