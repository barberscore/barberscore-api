# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20151206_2335'),
    ]

    operations = [
        migrations.RenameModel("Competitor", "Contestant")
    ]
