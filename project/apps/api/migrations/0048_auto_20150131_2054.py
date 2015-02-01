# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0047_auto_20150131_2043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chorus',
            name='prelim',
        ),
        migrations.RemoveField(
            model_name='chorus',
            name='rank',
        ),
        migrations.RemoveField(
            model_name='quartet',
            name='prelim',
        ),
        migrations.RemoveField(
            model_name='quartet',
            name='rank',
        ),
    ]
