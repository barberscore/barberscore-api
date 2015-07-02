# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0122_auto_20150701_2228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='is_score',
        ),
    ]
