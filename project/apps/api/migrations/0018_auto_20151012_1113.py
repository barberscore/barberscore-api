# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20151012_1040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='status',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='status_changed',
        ),
    ]
