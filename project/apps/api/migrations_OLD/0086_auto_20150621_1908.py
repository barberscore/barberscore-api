# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0085_auto_20150621_1857'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='name',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='slug',
        ),
    ]
