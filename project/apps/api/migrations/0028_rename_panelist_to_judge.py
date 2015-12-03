# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_auto_20151203_1250'),
    ]

    operations = [
        migrations.RenameModel('Panelist', 'Judge')
    ]
