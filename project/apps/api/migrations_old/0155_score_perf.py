# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0154_remove_score_performance'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='perf',
            field=models.ForeignKey(related_name='scores', blank=True, to='api.Performance', null=True),
        ),
    ]
