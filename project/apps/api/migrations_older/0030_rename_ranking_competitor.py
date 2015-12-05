# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_auto_20151203_1355'),
    ]

    operations = [
        migrations.RenameModel('Ranking', 'Competitor'),
    ]
