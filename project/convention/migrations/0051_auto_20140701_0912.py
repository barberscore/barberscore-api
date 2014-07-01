# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0050_remove_contestant_district'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contestant',
            old_name='district_id',
            new_name='district',
        ),
    ]
