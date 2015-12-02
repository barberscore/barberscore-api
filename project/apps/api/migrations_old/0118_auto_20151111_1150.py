# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0117_auto_20151111_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='start_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='session',
            name='start_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
