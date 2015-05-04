# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_performance_apperance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='performance',
            old_name='apperance',
            new_name='appearance',
        ),
    ]
