# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_auto_20151203_2058'),
    ]

    operations = [
        migrations.RenameModel('Panel', 'Contest'),
    ]
