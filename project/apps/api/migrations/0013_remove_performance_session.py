# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_remove_performance_convention'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='session',
        ),
    ]
