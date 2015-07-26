# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20150725_2133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupf',
            name='child',
        ),
        migrations.RemoveField(
            model_name='personf',
            name='child',
        ),
        migrations.RemoveField(
            model_name='songf',
            name='child',
        ),
    ]
