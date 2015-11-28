# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0148_auto_20151127_1619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='contestant',
        ),
    ]
