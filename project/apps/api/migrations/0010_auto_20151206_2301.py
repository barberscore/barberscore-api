# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20151206_2252'),
    ]

    operations = [
        migrations.RenameModel('Session', 'Round')
    ]
