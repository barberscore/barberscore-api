# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0138_auto_20151129_0618'),
    ]

    operations = [
        migrations.AddField(
            model_name='ranking',
            name='contest',
            field=models.ForeignKey(related_name='rankings', blank=True, to='api.Contest', null=True),
        ),
    ]
