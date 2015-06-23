# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0096_auto_20150623_1407'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='district',
            name='abbr',
        ),
    ]
