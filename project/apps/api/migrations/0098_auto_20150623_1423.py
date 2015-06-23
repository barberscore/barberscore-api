# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0097_remove_district_abbr'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contestant',
            old_name='total_raw',
            new_name='points',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='total_raw',
            new_name='points',
        ),
        migrations.RemoveField(
            model_name='group',
            name='director',
        ),
    ]
