# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_performance_aranger'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='aranger',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='person',
        ),
    ]
