# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0100_contestant_men'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='men',
        ),
    ]
