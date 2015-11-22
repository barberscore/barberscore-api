# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0124_auto_20151120_0608'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='performance',
            field=models.ForeignKey(related_name='sessions', blank=True, to='api.Performance', null=True),
        ),
    ]
