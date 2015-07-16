# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0149_performance_chart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='arranger',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='song',
        ),
    ]
