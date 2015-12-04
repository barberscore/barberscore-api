# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_auto_20151203_2030'),
    ]

    operations = [
        migrations.RenameModel('Contest', 'Award')
    ]
