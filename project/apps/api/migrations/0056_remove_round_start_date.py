# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0055_auto_20151220_2059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='round',
            name='start_date',
        ),
    ]
