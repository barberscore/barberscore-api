# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_auto_20151213_2130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='convention',
            name='orgs',
        ),
    ]
