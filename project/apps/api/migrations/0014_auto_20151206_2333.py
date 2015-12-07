# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20151206_2324'),
    ]

    operations = [
        migrations.RenameModel("Contestant", "Performer")
    ]
