# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20151206_2340'),
    ]

    operations = [
        migrations.RenameModel("Award", "Contest")
    ]
