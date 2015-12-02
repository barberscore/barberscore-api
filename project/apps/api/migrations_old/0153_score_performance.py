# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0152_auto_20151201_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='performance',
            field=models.ForeignKey(related_name='scores', blank=True, to='api.Performance', null=True),
        ),
    ]
